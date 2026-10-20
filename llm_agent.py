from groq import Groq

from dotenv import load_dotenv
import base64
import os


class ConversationAgent:
    def __init__(self):
        load_dotenv()
        self.groq_client = Groq(api_key=os.environ["GROQ_KEY"])
        self.text_model = "openai/gpt-oss-120b"
        self.vision_model = "qwen/qwen3.8-27b"
        self.conversation_history = [
                {
                    "role": "system",
                    "content": self.read_file(file_path="./context.txt")
                }
            ]


    @staticmethod
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()


    def get_conversation_history(self):
        return self.conversation_history[1: ]


    def update_conversation_history(self, role, content):
        self.conversation_history.append(
            {
            "role": role,
            "content": content,
            }
        )


    @staticmethod
    def encode_image(image_file):
        image_base64 = base64.b64encode(image_file.getvalue()).decode("utf-8")
        return f"data:{image_file.type};base64,{image_base64}"


    def conversation_has_images(self):
        return any(isinstance(message["content"], list) for message in self.conversation_history)


    def ask_llm(self, text_interaction, images=None):

        if images:
            content = []
            if text_interaction:
                content.append({"type": "text", "text": text_interaction})
            for image in images:
                content.append({"type": "image_url", "image_url": {"url": self.encode_image(image)}})
        else:
            content = text_interaction

        self.update_conversation_history(role="user", content=content)

        if self.conversation_has_images():
            response = self.groq_client.chat.completions.create(
                messages=self.conversation_history,
                model=self.vision_model,
            ).choices[0].message.content
        else:
            response = self.groq_client.chat.completions.create(
                messages=self.conversation_history,
                model=self.text_model,
                include_reasoning=False,
            ).choices[0].message.content


        self.update_conversation_history(role="assistant", content=response)
        return response





























if __name__ == "__main__":
    question = input("Pose ta question :\n")
    agent = ConversationAgent()
    response = agent.ask_llm(question)
    print("\n")
    print(response)