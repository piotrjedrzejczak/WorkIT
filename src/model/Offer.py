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
        return ('Offer:\n'
                f'Title: {self.title}\n'
                f'Company: {self.company}\n'
                f'City: {self.city}\n'
                f'Salary: {self.salary}\n'
                f'Tech Stack: {self.techstack}\n'
                f'Experience: {self.experience}\n'
                f'Logo URL: {self.logourl}\n'
                f'OfferURL: {self.offerurl}\n')
                
