from openai import OpenAI, AsyncOpenAI

import constants

DALLE_MODEL_NAME = "dall-e-2"


class DALLEClient:
    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=constants.OPENAI_API_KEY)

    async def generate_image(self, prompt):
        response = await self.client.images.generate(
        model=DALLE_MODEL_NAME,
        prompt=f"Create an image only of this dish: {prompt}. ",
        size="1024x1024",
        quality="standard",
        n=1,
    )
        
        image_url = response.data[0].url

        #For testing
        #image_url = "https://dummyimage.com/600x400/000/fff"
        
        return image_url
    

