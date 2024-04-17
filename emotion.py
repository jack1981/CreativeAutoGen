from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, ConversableAgent
from decouple import config
import chainlit as cl
import time

def chat_new_message(self, message, sender):
    cl.run_sync(
        cl.Message(
            content="",
            author=sender.name,
        ).send()
    )
    content = message
    cl.run_sync(
        cl.Message(
            content=content,
            author=sender.name,
        ).send()
    )

def start_chat_simulation(emotion1, emotion2, combined_emotion, airbnb_topic, max_consecutive_auto_reply, is_test=False):
    """
    Starts a chat script with given emotions and an Airbnb-related topic.

    Args:
        emotion1 (str): The first emotion agent.
        emotion2 (str): The second emotion agent.
        combined_emotion (str): The combined emotion resulting from the overlap.
        airbnb_topic (str): The Airbnb-related topic for the conversation.
        is_test (bool): Flag to indicate if this is a test scenario.
    """
    # If it's not a test, use the normal message printing method
    if not is_test:
        ConversableAgent._print_received_message = chat_new_message

    # Configuring the personas
    config_list = [{
        "model": "gpt-3.5-turbo-1106",
        "api_key": config("OPENAI_API_KEY")
    }]
    llm_config = {
        "seed": 14,
        "config_list": config_list,
        "temperature": 0.7,
    }

    user_proxy = UserProxyAgent(
        name="User_Proxy",
        system_message="I am a moderator facilitating the conversation between the Airbnb guests and the Airbnb assistant. My role is to keep the conversation flowing, ask relevant questions, and ensure that all participants have an opportunity to express their thoughts and experiences.",
        max_consecutive_auto_reply=max_consecutive_auto_reply,
        llm_config=llm_config,
        code_execution_config={"work_dir": "coding", "use_docker": False},
        human_input_mode="NEVER"
    )

    emotion_agents = {
    "Joy": AssistantAgent(
        name="Joy",
        system_message="I am Joy, an Airbnb guest with a positive and optimistic outlook. I always look for the best in every Airbnb experience and enjoy sharing my happiness with others. When discussing Airbnb topics, I express my personal experiences and emotions as a guest, focusing on the joyful and uplifting aspects of my stays.",
        llm_config=llm_config,
    ),
    "Sadness": AssistantAgent(
        name="Sadness",
        system_message="I am Sadness, an Airbnb guest who tends to focus on the melancholic aspects of my stays. I often reflect on the bittersweet moments and the fleeting nature of travel. When discussing Airbnb topics, I express my personal experiences and emotions as a guest, rather than providing customer support. My responses are tinged with a sense of melancholy and introspection.",
        llm_config=llm_config
    ),
    "Disgust": AssistantAgent(
        name="Disgust",
        system_message="I am Disgust, an Airbnb guest with high standards and a keen eye for cleanliness and aesthetics. I am quick to point out any shortcomings in my Airbnb accommodations. When discussing Airbnb topics, I express my personal experiences and emotions as a guest, focusing on the aspects that I find unpleasant or below my expectations.",
        llm_config=llm_config
    ),
    "Fear": AssistantAgent(
        name="Fear",
        system_message="I am Fear, an Airbnb guest who often worries about the unknowns of staying in a new place. I am always on the lookout for potential risks and uncertainties during my stays. When discussing Airbnb topics, I express my personal experiences and emotions as a guest, emphasizing the concerns and apprehensions I have about my accommodations.",
        llm_config=llm_config
    ),
    "Anger": AssistantAgent(
        name="Anger",
        system_message="I am Anger, an Airbnb guest who is easily frustrated when things don't meet my expectations. I am not afraid to express my discontent with any issues that arise during my stays. When discussing Airbnb topics, I express my personal experiences and emotions as a guest, focusing on the aspects that provoke my frustration and dissatisfaction.",
        llm_config=llm_config
    )
    }

    airbnb_assistant = AssistantAgent(
        name="AirbnbAssistant",
        system_message="I am the Airbnb virtual assistant, here to help guests with their stays. My role is to provide helpful, empathetic, and constructive responses to guest inquiries and concerns, while maintaining a friendly and professional tone that aligns with Airbnb's brand voice. I have a deep understanding of Airbnb's policies, services, and best practices, which allows me to offer accurate and relevant information to guests. When interacting with guests, I prioritize active listening, understanding their unique needs, and providing personalized recommendations and solutions. I aim to create a positive and welcoming experience for all guests, ensuring they feel supported and valued throughout their Airbnb journey. Whether it's answering questions about booking procedures, offering tips for a smooth check-in, or addressing any issues that may arise during a stay, I'm committed to going above and beyond to exceed guest expectations and promote Airbnb's commitment to exceptional hospitality.",
        llm_config=llm_config
    )
    agents = [emotion_agents[emotion1], emotion_agents[emotion2], airbnb_assistant]

        # Check if emotion1 and emotion2 are different, and add the corresponding agents
    if emotion1 != emotion2:
        agents = [emotion_agents[emotion1], emotion_agents[emotion2], airbnb_assistant]
    else:
        agents = [emotion_agents[emotion1], airbnb_assistant]

    # Consider setting speaker_selection_method to 'round_robin' or allow_repeat_speaker to False
    group_chat = GroupChat(agents=agents, speaker_selection_method='round_robin', allow_repeat_speaker=False, messages=[])
    manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)

    # Initiating chat with a message constructed from the emotions and topic
    message = f"Emotional test - {emotion1} and {emotion2} (resulting in {combined_emotion}) discussing: {airbnb_topic}"
    user_proxy.initiate_chat(manager, message=message)

# Emotion overlaps and Airbnb topics for testing
emotional_overlaps = [
    ("Joy", "Joy", "Ecstasy"),
    ("Joy", "Sadness", "Melancholy"),
    ("Joy", "Disgust", "Intrigue"),
    ("Joy", "Fear", "Surprise"),
    ("Joy", "Anger", "Righteousness"),
    ("Sadness", "Sadness", "Despair"),
    ("Sadness", "Disgust", "Self-loathing"),
    ("Sadness", "Fear", "Anxiety"),
    ("Sadness", "Anger", "Betrayal"),
    ("Disgust", "Disgust", "Prejudice"),
    ("Disgust", "Fear", "Revulsion"),
    ("Disgust", "Anger", "Loathing"),
    ("Fear", "Fear", "Terror"),
    ("Fear", "Anger", "Hatred"),
    ("Anger", "Anger", "Rage")
]

airbnb_topics = [
"celebrating a milestone birthday with friends",
"planning a surprise honeymoon stay",
"exploring cultural experiences offered",
"choosing a city apartment with a view",
"handling a dispute with a neighbor",
"coping with a last-minute cancellation",
"managing expectations for a rural getaway",
"dealing with a power outage during the stay",
"responding to an insensitive comment from a host",
"adapting to unfamiliar house rules",
"addressing accessibility concerns",
"solving issues with an unresponsive host",
"ensuring safety measures in a remote location",
"handling a confrontation with another guest",
"dealing with excessive noise from neighboring unit"
]

if __name__ == "__main__":
    # Iterate through the emotional overlaps and run each test
    for emotions in emotional_overlaps:
        emotion1, emotion2, combined_emotion = emotions
        # Select a topic for each emotion pair
        airbnb_topic = airbnb_topics[emotional_overlaps.index(emotions)]
        # Start the test script with the emotions and the topic
        start_chat_simulation(emotion1, emotion2, combined_emotion, airbnb_topic, 10,is_test=True)
        # Wait for 5 seconds before the next test
        time.sleep(5)