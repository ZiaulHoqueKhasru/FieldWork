import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
#gro_api_key=os.getenv("GROQ_API_KEY")

import tiktoken  # Install with: pip install tiktoken

from langdetect import detect  # You can install it with `pip install langdetect`

def generate_summary(news_body):
    def get_tokenizer_for_model(model):
        """Get the tokenizer for the specified model or fallback."""
        try:
            return tiktoken.encoding_for_model(model)
        except KeyError:
            return tiktoken.get_encoding("cl100k_base")

    def chunk_text(text, encoding, chunk_size):
        """Divide the text into manageable chunks."""
        tokens = encoding.encode(text)
        for i in range(0, len(tokens), chunk_size):
            yield encoding.decode(tokens[i:i + chunk_size])

    try:
        model = "mixtral-8x7b-32768"
        total_token_limit = 5000
        reserved_tokens = 1024
        chunk_size = total_token_limit - reserved_tokens
        max_tokens = 512

        encoding = get_tokenizer_for_model(model)
        chunks = list(chunk_text(news_body, encoding, chunk_size))
        summaries = []

        client = Groq()

        # Detect language (using langdetect)
        language = detect(news_body)

        if language == 'en':  # If English
            system_prompt = (
                "You are an expert summarizer. The input text is in English. Summarize the news concisely in English."
            )
        else:  # Default to Bengali for other languages, you can add more conditions
            system_prompt = (
                "You are an expert summarizer. The input text is in Bengali. Summarize the news concisely in Bengali."
            )

        for chunk in chunks:
            chat_completion = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": chunk,
                    },
                ],
                temperature=0,
                max_tokens=max_tokens,
                top_p=1,
                stream=False,
                stop=None,
            )
            summaries.append(chat_completion.choices[0].message.content)

        final_summary = "\n\n".join(summaries)
        return final_summary

    except Exception as e:
        return f"An error occurred: {e}"







if __name__ == '__main__':
    data = generate_summary('''
কিছুদিন আগেই আমন মৌসুমের চাল বাজারে উঠেছে। সাধারণত ভরা মৌসুমে চালের দাম কমে এলেও গত এক মাসে মাঝারি ও সরু চালের দাম বেড়েছে কেজিতে অন্তত ৪ থেকে ৮ টাকা পর্যন্ত। শীতকালীন ফসল ছাড়া অন্য সব পণ্যমূল্যের ঊর্ধ্বগতিতে চাপে থাকা ভোক্তারা এতে বাড়তি চাপে পড়েছেন।

গত বছরের একই সময়ের তুলনায় জাতভেদে চালের দাম কেজিতে ৪ টাকা থেকে ২০ টাকা পর্যন্ত বেড়েছে। অথচ সাধারণত বছরের এই সময়, যখন বোরোর পরে দ্বিতীয় বৃহত্তম ধানের উৎস আমন ধান কাটা হয়, প্রধান প্রধান চালের দাম কমে যায় অথবা অন্তত স্থির থাকে।

আশঙ্কা করা হয়েছিল, আগস্টে বেশ কয়েকটি জেলায় ব্যাপক বন্যার ফলে আমনের উৎপাদন ব্যাপক কমে যাবে। কিন্তু সরকারি তথ্য বলছে উল্টো কথা। কৃষি মন্ত্রণালয়ের দাবি, গত মৌসুমের তুলনায় চলতি বছর আমনের ফলন প্রায় ৫ লাখ টন বেশি। আমন মৌসুমের চাল ইতিমধ্যেই বাজারে পৌঁছেছে। তাহলে বাজারে কেন এত দাম বেড়েছে?

বাজার পর্যবেক্ষকরা বলছেন, মজুত কমে যাওয়া, স্থানীয় বাজার থেকে কম সংগ্রহ এবং আমদানি সিদ্ধান্তে বিলম্বের কারণে বাজারে কারসাজির সুযোগ তৈরি হয়েছে। মোটা, মাঝারি ও সরু—দেশের বাজারে মূলত এ তিন ক্যাটাগরির চাল পাওয়া যায়। খুচরা পর্যায়ে এসব ধানের  দাম এখন কেজিতে যথাক্রমে ৫৪-৫৮ টাকা, ৬২-৬৪ টাকা ও ৮২-৮৬ টাকা।

সরকারি সংস্থা ট্রেডিং করপোরেশন অভ বাংলাদেশের (টিসিবি) তথ্যানুযায়ী, গত বছরের এই সময়ে খুচরা বাজারে মোটা চাল ৫০-৫২ টাকা, মাঝারি চাল ৫২-৫৮ টাকা এবং সরু চাল ৬২-৭৫ টাকায় বিক্রি হয়েছে। 

মোটা চালের দাম, যা মূলত নিম্ন-আয়ের মানুষ খায়, খুব বেশি বাড়েনি। কিন্তু বাজারে মোটা চাল পাওয়া কঠিন। রাজধানীর বিভিন্ন বাজার ঘুরে দেখা যায়, মোটা চাল সব দোকানে পাওয়া যায় না। ঢাকার কারওয়ান বাজারের পাইকারি বিক্রেতারা জানান, গত দেড় মাসে মিনিকেটের দাম বেড়েছে সবচেয়ে বেশি, কেজিতে ১০-১৪ টাকা। 

কারওয়ান বাজারের চালের আড়তের পাইকারি বিক্রেতা মোশারফ হোসেন টিবিএসকে বলেন, '৬৬-৬৮ টাকার মিনিকেট এখন মিল থেকেই কিনে আনছি ৮০-৮২ টাকায়। এরপর আমাদের পরিবহন খরচ আছে। ব্যবসার খুব বাজে অবস্থা, ক্রেতা নেই। দাম বাড়লে আমাদের ক্রেতা থাকে না।' মধ্যম আয়ের পরিবারগুলোতে এই জাতটি জনপ্রিয়। চাল কেনার পেছনে তাদের মাসিক বাজেট বেড়েছে।

কারওয়ান বাজারে চাল কিনতে আসা একটি বেসরকারি প্রতিষ্ঠানের চাকরিজীবী মো. মহিউদ্দিন টিবিএসকে বলেন, 'এখন মিনিকেট ৫০ কেজির বস্তা ৪ হাজার ১০০ টাকা চাচ্ছে। কয়েকদিন আগেও ৩ হাজার ৫০০ থেকে ৩ হাজার ৬০০ টাকা ছিল। সবজি ছাড়া এখন বাজারে সবকিছুর দাম বেশি। চালের দামটা সহনীয় থাকলে মধ্যবিত্ত বা নিম্নবিত্তরা খেতে পারে। কিন্তু এটা তো একেবারে নিয়ন্ত্রণের বাইরে চলে যাচ্ছে।'

খাদ্যশস্যের মজুত বৃদ্ধির তাগিদ বুঝতে পেরে গত বছরের অক্টোবরে চাল আমদানির ওপর ৩৫ শতাংশ শুল্ক কমিয়েছিল সরকার। আশা করেছিল, আমদানি মূল্য ১৪.৫০ টাকা কমবে। কিন্তু বেসরকারি আমদানিকারকরা খুব বেশি আগ্রহ দেখায়নি। কারণ তারা হিসাব করে দেখেছে, শুল্ক কমানোর পরও আমদানি খরচ ৬৫ টাকা ছাড়িয়ে যাবে, যা স্থানীয় বাজারমূল্যের চেয়ে বেশি। যদিও সম্প্রতি চাল আমদানি নিয়ে জোর তৎপরতা চালাচ্ছে সরকার, তবু অনেক দেরি হয়ে গেছে। চলতি অর্থবছরে এখন পর্যন্ত মাত্র ২.৬৪ লাখ টন চাল আমদানি করা হয়েছে। ২০২২-২৩ অর্থবছরে আমদানি হয়েছিল ১০.৫৬ লাখ টন চাল। বিশ্লেষকরা বলছেন, আরও আগেই চাল আমদানির উদ্যোগ নেওয়া হলে চালের বাজারে এ অস্থিরতা দেখা দিত না।

            ''')

    print(data)