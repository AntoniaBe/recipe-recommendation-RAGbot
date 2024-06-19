from openai import OpenAI, AsyncOpenAI
import base64
import constants


VISION_MODEL_NAME = "gpt-4o"

class VisionClient:
    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=constants.OPENAI_API_KEY)

    @staticmethod
    def base64_image(image_file) -> bytes:
        return base64.b64encode(image_file.read()).decode('utf-8')

    async def describe_image(self, image_file: bytes) -> str:
            response = await self.client.chat.completions.create(
                model=VISION_MODEL_NAME,
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": "You are a master chef that creates delicious dishes."},
                    {"role": "user", "content": [
                        {
                            "type": "text",
                            "text": "Give me a simple list, of all the clearly identifiable ingredients you can see in the picture, without any additional text. Create three recipe recommondations with instructions, that utilize these ingredients. Return a json, containing the ingredients from the picture and the recipes with recipe_name, recipe_ingredients and recipe_instructions."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_file}"
                            }
                        }
                    ]}
                ],
                max_tokens=800
            )

            return response.to_dict()["choices"][0]["message"]["content"]

