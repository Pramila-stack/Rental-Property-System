why post() is necessary in detailview.

# 🧠 Why you need post() here

You are combining:
DetailView + FormView
👉 Django does NOT automatically connect form submission to your object.
So when a user submits the booking form:
Django calls POST
But:
DetailView doesn’t handle forms
FormView doesn’t know your Property
👉 So you must manually control the flow → that’s why post() is needed

# 👉 In a POST request, we use a form to: so thats why we used form=self.get_form()
1. Receive data
2. Validate data
3. Clean data
4. Save/process data


# 👉 We need GET and POST because:
GET = show the review form
POST = submit and save the review
So you want:
self.property
available everywhere.
🔥 So why dispatch()?
👉 Because dispatch() runs before BOTH GET and POST
request → dispatch() → get() OR post()

# ❗ What happens WITHOUT dispatch?

You would have to repeat:
❌ BAD
def get():
    property = get_object_or_404(...)

def post():
    property = get_object_or_404(...)

👉 Problems:
repeated code
more DB queries
higher chance of mistakes


# Why review used dispatch and booking did not.
🧠 Simple explanation
🏠 Booking:
👉 Django already knows:
which property
how to fetch it
how to pass it to template
So no extra setup needed.

⭐ Review:
👉 You manually said:
“I want this property stored globally in the view for both GET and POST”
So you used:
dispatch()


