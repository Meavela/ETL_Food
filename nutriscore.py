class Nutriscore:
    def __init__(self, nutrients):
        self.nutriscore = 0
        self.score = 0
        self.badPoints = 0
        self.goodPoints = 0
        self.nutrients = nutrients
        self.calculate_nutriscore()
    
    def calculate_nutriscore(self):
        # Bad points
        ## Energie
        energy = 0
        for i in range(len(self.nutrients)):
            if self.nutrients[i]['label'] == 'Energy':
                energy = self.nutrients[i]['value']
        ### 0 : <=335
        if energy <= 335:
            self.badPoints += 0
        ### 1 : >335
        elif energy > 335 and energy <= 670:
            self.badPoints += 1
        ### 2 : >670
        elif energy > 670 and energy <= 1005:
            self.badPoints += 2
        ### 3 : >1005
        elif energy > 1005 and energy <= 1340:
            self.badPoints += 3
        ### 4 : >1340
        elif energy > 1340 and energy <= 1675:
            self.badPoints += 4
        ### 5 : >1675
        elif energy > 1675 and energy <= 2010:
            self.badPoints += 5
        ### 6 : >2010
        elif energy > 2010 and energy <= 2345:
            self.badPoints += 6
        ### 7 : >2345
        elif energy > 2345 and energy <= 2680:
            self.badPoints += 7
        ### 8 : >2680
        elif energy > 2680 and energy <= 3015:
            self.badPoints += 8
        ### 9 : >3015
        elif energy > 3015 and energy <= 3350:
            self.badPoints += 9
        ### 10 : >3350
        elif energy > 3350:
            self.badPoints += 10
        ## Sucre
        sucre = 0
        for i in range(len(self.nutrients)):
            if self.nutrients[i]['label'] == 'Sugars':
                sucre = self.nutrients[i]['value']
        ### 0 : <=4.5
        if sucre <= 4.5:
            self.badPoints += 0
        ### 1 : >4.5
        elif sucre > 4.5 and sucre <= 9:
            self.badPoints += 1
        ### 2 : >9
        elif sucre > 9 and sucre <= 13.5:
            self.badPoints += 2
        ### 3 : >13.5
        elif sucre > 13.5 and sucre <= 18:
            self.badPoints += 3
        ### 4 : >18
        elif sucre > 18 and sucre <= 22.5:
            self.badPoints += 4
        ### 5 : >22.5
        elif sucre > 22.5 and sucre <= 27:
            self.badPoints += 5
        ### 6 : >27
        elif sucre > 27 and sucre <= 31:
            self.badPoints += 6
        ### 7 : >31
        elif sucre > 31 and sucre <= 36:
            self.badPoints += 7
        ### 8 : >36
        elif sucre > 36 and sucre <= 40:
            self.badPoints += 8
        ### 9 : >40
        elif sucre > 40 and sucre <= 45:
            self.badPoints += 9
        ### 10 : >45
        elif sucre > 45:
            self.badPoints += 10
        ## Acide gras saturés
        acideGrasSatures = 0
        for i in range(len(self.nutrients)):
            if self.nutrients[i]['label'] == 'Fatty acids, total saturated':
                acideGrasSatures = self.nutrients[i]['value']
        ### 0 : <=1
        if acideGrasSatures <= 1:
            self.badPoints += 0
        ### 1 : >1
        elif acideGrasSatures > 1 and acideGrasSatures <= 2:
            self.badPoints += 1
        ### 2 : >2
        elif acideGrasSatures > 2 and acideGrasSatures <= 3:
            self.badPoints += 2
        ### 3 : >3
        elif acideGrasSatures > 3 and acideGrasSatures <= 4:
            self.badPoints += 3
        ### 4 : >4
        elif acideGrasSatures > 4 and acideGrasSatures <= 5:
            self.badPoints += 4
        ### 5 : >5
        elif acideGrasSatures > 5 and acideGrasSatures <= 6:
            self.badPoints += 5
        ### 6 : >6
        elif acideGrasSatures > 6 and acideGrasSatures <= 7:
            self.badPoints += 6
        ### 7 : >7
        elif acideGrasSatures > 7 and acideGrasSatures <= 8:
            self.badPoints += 7
        ### 8 : >8
        elif acideGrasSatures > 8 and acideGrasSatures <= 9:
            self.badPoints += 8
        ### 9 : >9
        elif acideGrasSatures > 9 and acideGrasSatures <= 10:
            self.badPoints += 9
        ### 10 : >10
        elif acideGrasSatures > 10:
            self.badPoints += 10
        ## Sodium
        sodium = 0
        for i in range(len(self.nutrients)):
            if self.nutrients[i]['label'] == 'Sodium, Na':
                sodium = self.nutrients[i]['value']
        ### 0 : <=90
        if sodium <= 90:
            self.badPoints += 0
        ### 1 : >90
        elif sodium > 90 and sodium <= 180:
            self.badPoints += 1
        ### 2 : >180
        elif sodium > 180 and sodium <= 270:
            self.badPoints += 2
        ### 3 : >270
        elif sodium > 270 and sodium <= 360:
            self.badPoints += 3
        ### 4 : >360
        elif sodium > 360 and sodium <= 450:
            self.badPoints += 4
        ### 5 : >450
        elif sodium > 450 and sodium <= 540:
            self.badPoints += 5
        ### 6 : >540
        elif sodium > 540 and sodium <= 630:
            self.badPoints += 6
        ### 7 : >630
        elif sodium > 630 and sodium <= 720:
            self.badPoints += 7
        ### 8 : >720
        elif sodium > 720 and sodium <= 810:
            self.badPoints += 8
        ### 9 : >810
        elif sodium > 810 and sodium <= 900:
            self.badPoints += 9
        ### 10 : >900
        elif sodium > 900:
            self.badPoints += 10

        # Good points
        ## Fruits
        ## Fibres
        fibres = 0
        for i in range(len(self.nutrients)):
            if self.nutrients[i]['label'] == 'Fiber, total dietary':
                fibres = self.nutrients[i]['value']
        ### 0 : <=0.9
        if fibres <= 0.9:
            self.goodPoints += 0
        ### 1 : >0.9
        if fibres > 0.9 and fibres <= 1.9:
            self.goodPoints += 1
        ### 2 : >1.9
        if fibres > 1.9 and fibres <= 2.8:
            self.goodPoints += 2
        ### 3 : >2.8
        if fibres > 2.8 and fibres <= 3.7:
            self.goodPoints += 3
        ### 4 : >3.7
        if fibres > 3.7 and fibres <= 4.7:
            self.goodPoints += 4
        ### 5 : >4.7
        if fibres > 4.7:
            self.goodPoints += 5
        ## Protéines
        proteines = 0
        for i in range(len(self.nutrients)):
            if self.nutrients[i]['label'] == 'Protein':
                proteines = self.nutrients[i]['value']
        ### 0 : <=1.6
        if proteines <= 1.6:
            self.goodPoints += 0
        ### 1 : >1.6
        if fibres > 1.6 and fibres <= 3.2:
            self.goodPoints += 1
        ### 2 : >3.2
        if fibres > 3.2 and fibres <= 4.8:
            self.goodPoints += 2
        ### 3 : >4.8
        if fibres > 4.8 and fibres <= 6.4:
            self.goodPoints += 3
        ### 4 : >6.4
        if fibres > 6.4 and fibres <= 8.0:
            self.goodPoints += 4
        ### 5 : >8.0
        if proteines > 8.0:
            self.goodPoints += 5


        # Calcul du Nutri-Score
        score = self.badPoints - self.goodPoints
        if score <= 0 :
            self.nutriscore = "A"
        elif score >= 1 and score <= 10 :
            self.nutriscore = "B"
        elif score >= 11 and score <= 20 :
            self.nutriscore = "C"
        elif score >= 21 and score <= 30 :
            self.nutriscore = "D"
        elif score >= 31 and score <= 40 :
            self.nutriscore = "E"
