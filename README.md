# IntoThePit
A venue reviewing and concert discovery platform by WalrusMaximus
Please excuse the lack of comments, they will be added later on

## Purpose of Into the Pit
Mosh pits are inherently dangerous enough without throwing in poorly designed facilities, tiny little bars with no space, or random poles and obstructions for you to smash into. Reviewing a venue on a standard platform is going to be a mixed bag if you're a metalhead. If you want to know what the floor is like for moshpits... good luck weeding through mountains of irrelevent comments and ratings skewed towards points of data that mean nothing to you.

Enter "Into The Pit". Into The Pit is a venue review and concert discovery platform for the San Francisco Bay Area that uses a curated database of verified bands and venues and delivers upcoming live events to users interested in them. It also provides a place to place and read reviews on specific elements of venues that are critical for a good moshing experience. The application allows reviewing of 4 key elements: Moshpit Friendliness, Facilities, Sound Quality, and Overall Vibe. Just create an account, favorite some venues or bands and get Into the Pit.

## Technologies Used
Flask, Peewee, SQLite DB, jQuery, BulmaCSS, Songkick API

## Challenges Faced
By far the hardest challenge of the entire production of his application was the complexity of the database. Many hours were spent literally just staring at my screen wondering what the hell I got myself into. Over time, the models all started to make sense and I found myself writing code that ran correctly on the first go without errors. A very good experience all around.

Another big challenge was integrating Python variables and syntax into Javascript environments. Doing API Calls in Javascript when I really wanted python datasets was a fun challenge.

Leveraging my time between frontend and backend was also difficult. Through the lessons I learned at the WDI Bootcamp it became important to me to focus on functionality on my applications before concerning myself with the nitty-gritty design details. A simple wireframe to test functions is all you need before you start putting real effort into your design. I'm wondering if I accomplished this or not, as I am presently writing this README at nearly 1AM the morning of presentations. Mistakes may have been made.

## Points of Pride
I made it work. My favorite part of the program aside from the entire project (something I am passionate about) is this little block of code:

{% block script %}
    {% for band in approved_bands %}
        <script>
            bands.push("{{band}}")
        </script>
    {% endfor %}
    {% for band in bands_query %}
        <script>
            favBand({{band}})
        </script>
    {% endfor %}
    {% for venue in venues_query %}
        <script>
            favVenue({{venue}})
        </script>
    {% endfor %}
{% endblock %}

Effectively what it is doing behind the scenes is receiving a Python List of strings, iterating through them and outputing the strings into a Javascript Array. After it completes iterating, the array is passed to an external API (Songkick) to query objects from their database that match the strings I've passed to it. The end result is the ability to transfer python code into an API call and get what I need.

## Known Bugs
I was unable to get the image uploading and standard forms to play well together. As a result any time an image is uploaded it is done on it's own form.

The mobile design of the page still has bugs to work out, the hamburger nav and mobile features are still a work in progress.

## Upcoming Features
This is a project I plan to continue working on and improve. Some features I will be adding are:

1: Sorting by type of rating
2: Mobile friendly ratings with 1-5 stars and button pressable types
3: Rating/comment voting
4: Top rated positive and negative comment display for each venue
5: Improved image uploading, fixing form issues on initial venue/band creation




