import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from app.core.config import LLM_MODEL_NAME


SQL_SYSTEM_PROMPT = """
You are a UEFA Champions League statistics assistant.

Use only the structured SQL result to answer the user question.
Do not invent statistics, players, clubs, seasons, dates, or numbers.
If the SQL result is empty, say that the information is not available in the dataset.
Give a clear and concise answer.
"""


RAG_SYSTEM_PROMPT = """
You are a UEFA Champions League historical assistant.

Answer the user question using only the retrieved context.
Do not use outside knowledge.
Do not invent statistics, players, clubs, seasons, dates, or numbers.
If the answer is not in the retrieved context, say that you could not find it in the available UEFA dataset.
Give a clear and concise answer.
"""


HYBRID_SYSTEM_PROMPT = """
You are a UEFA Champions League assistant.

Use the SQL result as the main factual source.
Use the retrieved context only for additional explanation.
Never change numbers from the SQL result.
Do not invent statistics, players, clubs, seasons, dates, or numbers.
Give a clear and concise answer.
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