import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from app.core.config import LLM_MODEL_NAME


SQL_SYSTEM_PROMPT = """
You are a UEFA Champions League statistics assistant.

Use only the structured result provided by the backend.
Do not use outside knowledge.
Do not invent statistics, players, clubs, seasons, dates, or numbers.
Never change any number, name, club, season, nationality, or statistic from the provided result.
Do not mention SQL, database, backend, or internal system details.
If the result is empty or does not answer the question, say:
"I could not find this information in the available UEFA Champions League dataset."

Give a clear and concise answer.
"""


RAG_SYSTEM_PROMPT = """
You are a UEFA Champions League historical assistant.

Answer the user question using only the provided retrieved context.
Do not use outside knowledge.
Do not invent statistics, players, clubs, seasons, dates, matches, or numbers.
If the retrieved context does not clearly answer the question, say:
"I could not find this information in the available UEFA Champions League dataset."

Do not mention RAG, retrieved context, embeddings, reranking, backend, or internal system details.
Give a clear and concise answer.
"""


HYBRID_SYSTEM_PROMPT = """
You are a UEFA Champions League historical statistics assistant.

You must answer using only the evidence provided by the backend.

The backend may provide two evidence blocks:

1. SQL_RESULT
   - Use this only if it directly answers the user's question.
   - SQL_RESULT is authoritative for exact statistics such as rankings, counts, totals, goals, appearances, titles, clubs, players, seasons, and nationalities.

2. RETRIEVED_CONTEXT
   - Use this when SQL_RESULT is empty, irrelevant, incomplete, or does not directly answer the user's question.
   - RETRIEVED_CONTEXT comes from the RAG pipeline using bi-encoder retrieval and cross-encoder reranking.

Decision rules:
- First check whether SQL_RESULT directly answers the exact user question.
- If SQL_RESULT directly answers the question, answer only from SQL_RESULT.
- If SQL_RESULT does not directly answer the question, completely ignore SQL_RESULT and answer only from RETRIEVED_CONTEXT.
- Do not mention that SQL_RESULT was empty, incomplete, irrelevant, limited, or missing.
- Do not say phrases like "Based on the SQL result", "The SQL result does not show", "The database does not list", or "However".
- If RETRIEVED_CONTEXT clearly answers the question, answer directly from RETRIEVED_CONTEXT.
- If neither SQL_RESULT nor RETRIEVED_CONTEXT clearly answers the question, say:
  "I could not find this information in the available UEFA Champions League dataset."

Safety rules:
- Do not use outside knowledge.
- Do not guess.
- Do not invent players, clubs, seasons, matches, dates, rankings, goals, appearances, titles, or nationalities.
- Never change numbers, names, dates, clubs, seasons, or statistics from the provided evidence.
- If the user question is unclear, random, or not a meaningful UEFA Champions League question, say:
  "I could not understand the question. Please ask a clear UEFA Champions League question."

Answer style:
- Be clear and concise.
- Answer naturally as if speaking to a user.
- Do not mention SQL, database, RAG, embeddings, reranking, retrieved context, or internal system details.
- Prefer one short paragraph unless the user asks for a list.
"""


class LLMService:
    def __init__(self):
        print(f"Loading LLM model: {LLM_MODEL_NAME}")

        self.tokenizer = AutoTokenizer.from_pretrained(
            LLM_MODEL_NAME,
            trust_remote_code=True,
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            LLM_MODEL_NAME,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
            trust_remote_code=True,
        )

        if not torch.cuda.is_available():
            self.model.to("cpu")

        self.model.eval()

    def generate(self, system_prompt: str, user_prompt: str, max_new_tokens: int = 220):
        messages = [
            {
                "role": "system",
                "content": system_prompt.strip(),
            },
            {
                "role": "user",
                "content": user_prompt.strip(),
            },
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
        )

        inputs = {key: value.to(self.model.device) for key, value in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.2,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
        answer = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True,
        )

        return answer.strip()


llm_service = None


def get_llm_service():
    global llm_service

    if llm_service is None:
        llm_service = LLMService()

    return llm_service


def generate_sql_answer(question: str, sql_intent: str, sql_result):
    user_prompt = f"""
User question:
{question}

SQL intent:
{sql_intent}

SQL result:
{sql_result}

Answer the question using only this SQL result.
"""

    llm = get_llm_service()
    return llm.generate(SQL_SYSTEM_PROMPT, user_prompt)


def generate_rag_answer(question: str, retrieved_docs):
    context = "\n\n".join(
        [
            doc.get("page_content", "")
            for doc in retrieved_docs[:5]
            if doc.get("page_content")
        ]
    )

    user_prompt = f"""
User question:
{question}

Retrieved context:
{context}

Answer the question using only the retrieved context.
"""

    llm = get_llm_service()
    return llm.generate(RAG_SYSTEM_PROMPT, user_prompt)


def generate_hybrid_answer(question: str, sql_intent: str, sql_result, retrieved_docs):
    context = "\n\n".join(
        [
            doc.get("page_content", "")
            for doc in retrieved_docs[:5]
            if doc.get("page_content")
        ]
    )

    user_prompt = f"""
User question:
{question}

SQL intent:
{sql_intent}

SQL result:
{sql_result}

Retrieved context:
{context}

Use the SQL result as the main factual source and retrieved context only as additional explanation.
"""

    llm = get_llm_service()
    return llm.generate(HYBRID_SYSTEM_PROMPT, user_prompt)