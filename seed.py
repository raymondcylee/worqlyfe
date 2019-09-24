from models.medal import Medal
from models.badge import Badge

Badge(badge = "https://image.flaticon.com/icons/svg/1885/1885634.svg", badge_caption = "Standards raised!").save()  
Badge(badge = "https://image.flaticon.com/icons/svg/1530/1530884.svg", badge_caption = "Number 1!").save()
Badge(badge = "https://image.flaticon.com/icons/svg/2057/2057747.svg", badge_caption = "Awesome team player!").save()
Badge(badge = "https://image.flaticon.com/icons/svg/2057/2057748.svg ", badge_caption = "Thanks for the support!").save()
Badge(badge = "https://image.flaticon.com/icons/svg/1980/1980762.svg", badge_caption = "Great initiative!").save()
Badge(badge = "https://image.flaticon.com/icons/svg/2041/2041051.svg", badge_caption = "Lightning fast!").save()
Badge(badge = "https://image.flaticon.com/icons/svg/470/470238.svg", badge_caption = "Great job!").save()

Medal(medal="https://image.flaticon.com/icons/svg/179/179250.svg", medal_caption="Bronze").save()
Medal(medal="https://image.flaticon.com/icons/svg/179/179251.svg", medal_caption="Silver").save()
Medal(medal="https://image.flaticon.com/icons/svg/179/179249.svg", medal_caption="Gold").save()
Medal(medal="https://image.flaticon.com/icons/svg/167/167747.svg", medal_caption="Star").save()