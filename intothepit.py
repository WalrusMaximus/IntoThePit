from app import app
from app import models

if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='walrus',
            email="wal@rus.com",
            password='password',
            city="Oakland",
            state="California",
            zip="94601",
            user_level="walrus"
        )
        models.User.create_user(
            username='matt',
            email="ma@tt.com",
            password='password',
            city="Oakland",
            state="California",
            zip="94601",
        )
        models.Band.create_band(
            name="The Fantastic Walruses",
            about="They're a bunch of walruses",
            genre="Heavy Ivory",
            themes="data science is weird"
        )
        models.Venue.create_venue(
            name="The Iceberg",
            about="It's a venue for arctic creatures",
            address="225 Bush st",
            city="San Francisco",
            state="California",
            zip="94104"
        )
        models.Rating.create_rating(
            user_fk=1,
            venue_fk=1,
            rating=5,
            message="It's a place."
        )
    except ValueError:
        pass
        
    app.run(debug=True, port=8000)