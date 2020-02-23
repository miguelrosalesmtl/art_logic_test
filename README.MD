# Encoder Test

## Install

install requirements

pip install -r requirements.txt

## Run main

python main.py 

## Run Tests

python -m pytest

## feedback from part 1
1. You do not check for valid input on decoding (other than each arg is a base16 value), .e.g, I can write decode('aaaaa', 'bbbbbb') and it will return 5864062565883.

    ANSWER: I now use a regex to validate a hex string

2. It's wonderful you're using bit-arithmetic but consider in a production environment, writing:

         low = number & 0b0000000001111111 # mask

Is hard to read and error prone (I have to count the 1s and all the leading 0s are noise).  Whereas writing the following is concise:

         low = number & 0x7f # mask

Related, you don't need to use arithmetic.  In fact, doing so is confusing 
(imho) when what you really are doing is turning off bits.  That is, instead of:

         high = (number - low)<<1

Consider:

         high = (number  & 0x3f80) << 1

    ANSWER: Switched everything to hex

3. You have a bug in your MaximumValueError exception class which you don't see because of your usage.  Your constructor:

     def __init__(self, args):
         if args is None:
             self.message = args[0]
         else:
             self.message = None

if args is None you certainly couldn't access element 0 of it!  You'll note, none of your raised exceptions actually print the message you give. More generally, your class is not idiomatic subclassing  of Exception.

	ANSWER: I didn't think you were going to look at my tests in detail. In any case, I changed them and organized them differently

4. Lastly, while it's wonderful you provided unit tests, you only test "good" values.  Unit tests should also include the unexpected.  What happens if encode('fubar') is called?
	ANSWER: Added some more tests.

1. Tell us about something that you recently learned (or are currently learning). How do you approach
learning a new skill?
	ANSWER: I'm currently learning kubernetes more in depth, I tend to follow tutorials and read books.
	When I get stuck you just approach the problem from a different angle. Persistance is the key IMHO.
	I also like to teach or help others on their projects, in the long run it helps you to have a better
	understanding.

2. Describe the differences between projects you've been involved with (or seen) that have succeeded, and
those that have not been successful.
	ANSWER: I define success with customer satisfaction, the important thing is to keep the client happy. The important thing
	is to keep a good communication between the customer and the team and involve as much as possible the stakeholders. I've seen a 100k+ failing project, a director took all the decisions without involving the clients. Developers litteraly had no communication for months with stakeholders. Eventually, he called a meeting and showed them the software everyone was disapointed. The project was then cancelled. On that fiscal year he didn't even want to ask for R&D tax credits because he would have to show paperwork he didn't even do. To sum up, organization and communication.


3. The languages, tools, and technologies that we use as developers are always changing. What specific
languages/frameworks/platforms should developers be learning now to be ready for the next few years?
	ANSWER: Anything related to kubernetes really and distributed systems. Cloud services (Azure, GCE, AWS), Spark, Kafka, GraphQL, IBM Q. In terms of languages: Python, Kotlin, .NET Core. I think most technologies take on average 3 months of continous work to fully understand and be very comfortable with. That is also why that technologies can deprecate over night.

4. Discuss the most effective team you've been a part of. What made it so? What was your role on the
team?
	ANSWER: It is hard to say. In general, I am quite good when dealing with clients understanding their needs and what is appropriate for them. I developed interfaces for electronic work orders with 2 other people. I was the person calling the meetings and dealing with the requirements I think I did really well.

5. What specific approaches or techniques do you use in your code to make sure that it's bug-free and
performant?
	ANSWER: In theory it is impossible to have bug free code. When it comes to performance, I really focus on what is important for the customer and what he wants to achieve and try to think of the future. I don't care much about execution time of the code, unless it is a requirement or can be a source of problems when the system scales up, very fast code is not readable.
My methods almost never go beyond 50 lines, I write tests, consult others, try to keep my code clean (no random comments). 
