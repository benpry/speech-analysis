from guizero import App, PushButton, Slider, Text


def start_recording():
    """Prepares the recording and notifies the user to talk."""
    message.value = "Start Speaking Please!"
    print('hello will')


app = App(title="Speech Improve", bg="pink")
message = Text(app, text="Welcome to Speech Improve!")
button = PushButton(app, command=start_recording)
app.display()
