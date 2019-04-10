from app import app
from app import models

if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='walrus',
            email="wal@rus.com",
            password='password',
            avatar="images/user_walrus.png",
            user_level="walrus"
        )
        models.User.create_user(
            username='matt',
            email="ma@tt.com",
            password='password',
        )
        models.Band.create_band(
            name="Skeletonwitch",
            about="They are hella metal - Walrus",
            genre="Hella Metal",
            themes="data science is weird",
            img="images/band_skeletonwitch.jpg",
            skid="527207"
        )
        models.Band.create_band(
            name="Hypocrisy",
            about="Swedes make pretty solid metal",
            genre="Swedish Death Metal",
            themes="metal",
            img="images/band_hypocrisy.jpg",
            skid="433483"
        )
        models.Venue.create_venue(
            name="The Independent",
            about="Been there. It's alright.",
            img="images/venue_the_independent.jpg",
            skid="324"
        )
        models.Venue.create_venue(
            name="Oakland Metro Operahouse",
            about="Best venue ever",
            img="images/venue_oakland_metro_operahouse.jpg",
            skid="9809"
        )

    except ValueError:
        pass
        
    app.run(debug=True, port=8000)