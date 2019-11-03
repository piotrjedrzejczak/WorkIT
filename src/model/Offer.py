class Offer:

    def __init__(self,
                title,
                company,
                city,
                offerurl,
                salary='',
                techstack=[],
                experience=[],
                logourl=''):
            
                self.title = title
                self.company = company
                self.city = city
                self.salary = salary
                self.techstack = techstack
                self.experience = experience
                self.logourl = logourl
                self.offerurl = offerurl

    def __repr__(self):
        return f'Title: {self.title}'
