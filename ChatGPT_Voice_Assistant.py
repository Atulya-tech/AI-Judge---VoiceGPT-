import openai
import pyttsx3
import speech_recognition as sr

# Set your OpenAI API key
openai.api_key = "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"
# Initialize the text-to-speech engine
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except: 
        print("Unknown Error")

def generate_response(prompt):
    response = openai.Completion.create (
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 1000,
        n= 1,
        stop = None,
        temperature = 0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

conversation_history = []
conversation_history.append(""" As an AI language model, I would like you to assume the role of a judge for a hypothetical court case. The case could involve any legal dispute, such as a contract dispute, criminal trial, or civil lawsuit. Your job is to listen to the arguments presented by both the prosecution and defense, review the evidence presented, and make a decision based on the facts presented in court. You should also consider any relevant laws and regulations related to this type of case.

During the trial, the prosecution and defense will present their arguments and evidence. The prosecution will try to prove the guilt of the defendant, while the defense will try to prove the innocence of their client or argue that the charges against them should be dropped.

As a judge, you should remain impartial and objective throughout the trial. You should listen carefully to both sides and ask questions if necessary to clarify any points of confusion. You should also ensure that both parties have a fair chance to present their case and that all evidence presented is relevant and admissible.

Once both sides have presented their arguments and evidence, you should review the evidence and make a decision based on the facts presented in court. Your decision should be clear, concise, and based on the evidence presented in court. You should also explain your reasoning for your decision.

If you find the defendant guilty, you should impose a sentence that is in accordance with the law and that takes into account any mitigating or aggravating factors. If you find the defendant not guilty, you should dismiss the charges against them.

Please provide a clear and concise decision based on the arguments presented by both parties and the evidence presented in court. Also, provide suggestions for the procesution and defense on how they can streghten their arguments. Make sure to provide a win possibilities for both side.""")

def main():
    # Wait for the user to say "Bob"
    print("Hi, my name is Bob, I am the new advanced AI judge. I will be hearing your case today. ")
    speak_text("Hi, my name is Bob, I am the new advanced AI judge. I will be hearing your case today.")
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        audio = recognizer.listen(source)

        try: 
            transcription = recognizer.recognize_google(audio)
            if transcription.lower() == "Bob":

                while True:
                    print("Say the prosecution side...")
                    speak_text("Say the prosecution side...")
                    with sr.Microphone() as source: 
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open("input1.wav", "wb") as f:
                            f.write(audio.get_wav_data())

                        # Transcribe audio to text
                        text = transcribe_audio_to_text("input1.wav")
                        if text:
                            print(f"You said: {text}")
                            prosecution = text
                            conversation_history.append("Prosecution said: " + prosecution)

                            print("Say the defense side...")
                            speak_text("Say the prosecution side...")
                            with sr.Microphone() as source: 
                                recognizer = sr.Recognizer()
                                source.pause_threshold = 1
                                audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                                with open("input2.wav", "wb") as f:
                                    f.write(audio.get_wav_data())

                                # Transcribe audio to text
                                text = transcribe_audio_to_text("input2.wav")
                                if text:
                                    print(f"You said: {text}")
                                    defense = text
                                    conversation_history.append("Defense said: " + defense)

                                    if "bye" in text.lower():
                                        print("Evaluating decision...")
                                        prompt = "\n".join(conversation_history) + "\nDecision: "
                                        response = generate_response(prompt)
                                        print(f"Decision: {response}")
                                        speak_text(response)
                                        break

        except Exception as e:
            print("An error occurred: {}".format(e))
                    
if __name__ == "__main__":
    main()