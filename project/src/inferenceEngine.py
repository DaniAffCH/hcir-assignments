import pyAgrum as gum
import pyAgrum.lib.notebook as gnb
from utils_ import Dorms

class InferenceEngine:
    
    def __init__(self):
        bn = gum.BayesNet('Student Dorms')
        dorm_1 = Dorms("Bismarkstrasse", "Bismarkstrasse 4", "Bonn", "46 Single room in shared flat and 8 Double-Apartments", "from 289 to 436 euros for s Single room and from 507 to 812 euros for a Double-Apartement")
        dorm_2 = Dorms("Drussusstrasse", "Drussusstrasse 17", "Bonn", "73 Apartements", "from 245 to 642 euros")
        dorm_3 = Dorms("Europaring", "Europaring 2", "Sankt Augustin", "49 Apartements", "from 346 to 493 euros")
        dorm_4 = Dorms("StuHaus", "StuHaus", "Sankt Augustin", "106 Double or Shared Apartments and 60 Single Apartments", "from 395 to 413 euros for a Double Apartment and from 493 to 496 euros for a Single Apartment")
        dorm_5 = Dorms("Keramikerstrasse", "Keramikerstrasse 38", "Rheinbach", "30 Apartments ", "from 336 to 472 euros")
        dorm_6 = Dorms("Wg_gesucht", "Wg_gesucht", "Rheinbach", "Single room in shared flat", "from 400 to 500 euros" )

        self.dorm_names = [dorm_1, dorm_2, dorm_3, dorm_4, dorm_5, dorm_6]
        limited_budget = bn.add(gum.LabelizedVariable('limited_budget', 'Limited Budget', ['True', 'False']))
        pay_more_for_own_flat = bn.add(gum.LabelizedVariable('pay_more_for_own_flat', 'Pay more for own flat', ['True', 'False']))
        shared_common_space = bn.add(gum.LabelizedVariable('shared_common_space', 'Shared Common Space', ['True', 'False']))
        uni_location = bn.add(gum.LabelizedVariable('uni_location', 'University location', ['University of Bonn','HBRS in Sankt Augustin','HBRS in Rheinbach']))
        expensive = bn.add(gum.LabelizedVariable('expensive', 'Expensive', ['True', 'False']))
        loc_pref = bn.add(gum.LabelizedVariable('location_preference', 'Location Preference', ['Bonn', 'Sankt Augustin', 'Rheinbach']))
        is_social = bn.add(gum.LabelizedVariable('is_social', 'Is Social', ['True', 'False']))
       
        self.student_dorm = bn.add(gum.LabelizedVariable('student_dorm', 'Student Dorm', ['Bismarkstrasse 4', 'Drussusstrasse 17', 'Europaring 2', 'StuHaus', 'Keramikerstrasse 38', 'Wg_gesucht']))

        bn.addArc(limited_budget,expensive)
        bn.addArc(pay_more_for_own_flat,expensive)
        bn.addArc(pay_more_for_own_flat,is_social)
        bn.addArc(shared_common_space,is_social)
        bn.addArc(uni_location,loc_pref)
        bn.addArc(is_social,loc_pref)
        bn.addArc(expensive,loc_pref)

        bn.addArc(loc_pref,self.student_dorm)
        bn.addArc(is_social,self.student_dorm)
        bn.addArc(expensive,self.student_dorm)

        bn.cpt(limited_budget).fillWith([0.8,0.2])
        bn.cpt(pay_more_for_own_flat).fillWith([0.7,0.3])
        bn.cpt(shared_common_space).fillWith([0.5,0.5])
        bn.cpt(uni_location).fillWith([0.333, 0.333, 0.334])

        bn.cpt(expensive)[{"limited_budget": "True", "pay_more_for_own_flat": "True"}] = [0.5, 0.5]
        bn.cpt(expensive)[{"limited_budget": "False", "pay_more_for_own_flat": "False"}] = [0.1, 0.9]    
        bn.cpt(expensive)[{"limited_budget": "False", "pay_more_for_own_flat": "True"}] = [0.9, 0.1]
        bn.cpt(expensive)[{"limited_budget": "True", "pay_more_for_own_flat": "False"}] = [0.1, 0.9]

        bn.cpt(is_social)[{"pay_more_for_own_flat": "True", "shared_common_space": "True"}] = [0.5, 0.5]
        bn.cpt(is_social)[{"pay_more_for_own_flat": "False", "shared_common_space": "False"}] = [0.2, 0.8]
        bn.cpt(is_social)[{"pay_more_for_own_flat": "True", "shared_common_space": "False"}] = [0.9, 0.1]
        bn.cpt(is_social)[{"pay_more_for_own_flat": "False", "shared_common_space": "True"}] = [0.1, 0.9]
        
        bn.cpt(loc_pref)[{"expensive": "True","uni_location": "University of Bonn", "is_social": "True"}] = [0.8, 0.1, 0.1]
        bn.cpt(loc_pref)[{"expensive": "False","uni_location": "HBRS in Sankt Augustin", "is_social": "False"}] = [0.1, 0.1, 0.8]
        bn.cpt(loc_pref)[{"expensive": "True","uni_location": "HBRS in Rheinbach", "is_social": "True"}] = [0.1, 0.1, 0.8]
        bn.cpt(loc_pref)[{"expensive": "False","uni_location": "University of Bonn", "is_social": "False"}] = [0.1, 0.8, 0.1]
        bn.cpt(loc_pref)[{"expensive": "True","uni_location": "HBRS in Sankt Augustin", "is_social": "True"}] = [0.1, 0.8, 0.1]
        bn.cpt(loc_pref)[{"expensive": "False","uni_location": "HBRS in Rheinbach", "is_social": "False"}] = [0.8, 0.1, 0.1]
        bn.cpt(loc_pref)[{"expensive": "False","uni_location": "University of Bonn", "is_social": "True"}] = [0.8, 0.1, 0.1]
        bn.cpt(loc_pref)[{"expensive": "True","uni_location": "HBRS in Sankt Augustin", "is_social": "False"}] = [0.1, 0.1, 0.8]
        bn.cpt(loc_pref)[{"expensive": "True","uni_location": "HBRS in Rheinbach", "is_social": "False"}] = [0.8, 0.1, 0.1]
        bn.cpt(loc_pref)[{"expensive": "True","uni_location": "University of Bonn", "is_social": "False"}] = [0.1, 0.8, 0.1]
        bn.cpt(loc_pref)[{"expensive": "False","uni_location": "HBRS in Sankt Augustin", "is_social": "True"}] = [0.1, 0.8, 0.1]
        bn.cpt(loc_pref)[{"expensive": "False","uni_location": "HBRS in Rheinbach", "is_social": "True"}] = [0.1, 0.1, 0.8]
           
        bn.cpt(self.student_dorm)[{"expensive": "True", "location_preference": "Bonn","is_social": "True" }] = [0.1, 0.1, 0.1, 0.1, 0.1, 0.5]
        bn.cpt(self.student_dorm)[{"expensive": "True", "location_preference": "Bonn","is_social": "False" }] = [0.1, 0.1, 0.1, 0.1, 0.5, 0.1]
        bn.cpt(self.student_dorm)[{"expensive": "True", "location_preference": "Rheinbach","is_social": "True" }] = [0.1, 0.1, 0.1, 0.1, 0.1, 0.5]
        bn.cpt(self.student_dorm)[{"expensive": "True", "location_preference": "Rheinbach","is_social": "False" }] = [0.1, 0.1, 0.1, 0.5, 0.1, 0.1]
        bn.cpt(self.student_dorm)[{"expensive": "True", "location_preference": "Sankt Augustin","is_social": "False" }] = [0.1, 0.1, 0.1, 0.1, 0.1, 0.5]
        bn.cpt(self.student_dorm)[{"expensive": "True", "location_preference": "Sankt Augustin","is_social": "True" }] = [0.1, 0.1, 0.5, 0.1, 0.1, 0.1]
       
        bn.cpt(self.student_dorm)[{"expensive": "False", "location_preference": "Bonn","is_social": "False" }] = [0.1, 0.1, 0.1, 0.5, 0.1, 0.1]
        bn.cpt(self.student_dorm)[{"expensive": "False", "location_preference": "Bonn","is_social": "True"}] = [0.1, 0.1, 0.1, 0.1, 0.1, 0.5]
        bn.cpt(self.student_dorm)[{"expensive": "False", "location_preference": "Sankt Augustin","is_social": "False" }] = [0.1, 0.1, 0.1, 0.1, 0.1, 0.5]  
        bn.cpt(self.student_dorm)[{"expensive": "False", "location_preference": "Sankt Augustin","is_social": "True"}] = [0.1, 0.1, 0.1, 0.1, 0.5, 0.1]
        bn.cpt(self.student_dorm)[{"expensive": "False", "location_preference": "Rheinbach","is_social": "False" }] = [0.1, 0.1, 0.1, 0.1, 0.1, 0.5]
        bn.cpt(self.student_dorm)[{"expensive": "False", "location_preference": "Rheinbach","is_social": "True" }] = [0.1, 0.1, 0.1, 0.1, 0.5, 0.1]

        self.ie = gum.LazyPropagation(bn)

    def __call__(self, limited_budget: str, pay_more_for_own_flat: str, shared_common_space: str, uni_location:str):
        self.ie.setEvidence({'limited_budget': limited_budget, 'pay_more_for_own_flat': pay_more_for_own_flat, 'shared_common_space': shared_common_space, 'uni_location': uni_location})
        self.ie.makeInference()
        d = self.ie.posterior(self.student_dorm)
        mappedDorms = list(zip(self.dorm_names, d))
        sortedMappedDorms = sorted(mappedDorms, key=lambda x: x[1], reverse=True)
        return sortedMappedDorms

