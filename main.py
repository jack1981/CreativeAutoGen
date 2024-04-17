import chainlit as cl
from chainlit.input_widget import Select,Slider
from emotion import start_chat_simulation

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

@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="Emotional Agents Simulation",
            markdown_description="Get your group conversation with Emotional AI Characters and Agents",
        )
    ]

@cl.on_chat_start
async def on_chat_start():
    chat_profile = cl.user_session.get("chat_profile")
    await cl.Message(
        content=f"Welcome to {chat_profile} chat. Please select an emotion overlap and type your Airbnb-related topic in the message bar to get started."
    ).send()

    settings = await cl.ChatSettings(
        [
            Select(
                id="emotion_overlap",
                label="Select an emotion overlap:",
                values=[f"{e1},{e2},{ce}" for e1, e2, ce in emotional_overlaps],
                labels=[f"{e1} and {e2} results in {ce}" for e1, e2, ce in emotional_overlaps],
            ),
            Slider(
                id="max_consecutive_auto_reply",
                label="Max Consecutive Auto Reply",
                initial=10,
                min=5,
                max=50,
                step=1,
            )
        ]
    ).send()

@cl.on_settings_update
async def setup_agent(settings):
    print("on_settings_update", settings)
    emotion_overlap = settings.get("emotion_overlap")
    max_consecutive_auto_reply = settings.get("max_consecutive_auto_reply")
    cl.user_session.set("emotion_overlap", emotion_overlap)
    cl.user_session.set("max_consecutive_auto_reply", max_consecutive_auto_reply)

@cl.on_message
async def on_message(message):
    chat_profile = cl.user_session.get("chat_profile")
    message_content = message.content

    emotion_overlap = cl.user_session.get("emotion_overlap")
    max_consecutive_auto_reply = cl.user_session.get("max_consecutive_auto_reply")

    if emotion_overlap:
        emotion1, emotion2, combined_emotion = emotion_overlap.split(",")
        airbnb_topic = message_content
        start_chat_simulation(emotion1, emotion2, combined_emotion, airbnb_topic, max_consecutive_auto_reply)
    else:
        await cl.Message(
            content="Please select an emotion overlap before starting the conversation.",
        ).send()