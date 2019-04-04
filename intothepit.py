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
            name="The Fantastic Walruses",
            about="They're a bunch of walruses",
            genre="Heavy Ivory",
            themes="data science is weird",
            img="images/band_thefantasticwalruses.jpg",
            bg_img="images/band_bg_thefantasticwalruses.jpg"
        )
        models.Band.create_band(
            name="Not Walruses",
            about="They're not walruses",
            genre="lame",
            themes="data science is weird"
        )
        models.Venue.create_venue(
            name="The Iceberg",
            about="It's a venue for arctic creatures",
            address="225 Bush st",
            img="images/venue_theiceberg.jpg",
            city="San Francisco",
            state="California",
            zip="94104"
        )
        models.Venue.create_venue(
            name="Lame Venue",
            about="It's a venue for lame people",
            address="225 Bush st",
            city="San Francisco",
            state="California",
            zip="94104"
        )

    except ValueError:
        pass
        
    app.run(debug=True, port=8000)