# Ici on importe le module PySide2, il va nous permmettre de faire notre interface graphique pour notre application
from PySide2 import QtWidgets
# Nous importons le module qui va nous permettre de recup toutes les devises
import currency_converter

# Nous créons une classe qui va hériter d'un autre module de QtWidgets pour initialiser par la suite des fenêtres
class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Ici nous utilisons un attribut qui existe déjà dans la classe parent mais nous le mettons avec self pour
        # le définir sur l'instance également et qu'il soit automatique
        self.setWindowTitle("Convertisseur de Données")
        # Nous amenons la méthode setup_ui directement ici pour dire que cela appartiant automatique à l'instance
        self.setup_ui()
        # Voici une méthode pour changer le css de l'interface
        self.setup_css()
        # Grâce à cette méthode, on peut redefinir la taille de notre fenêtre
        self.resize(500, 50)
        # Nous crééons une variable qui va contenir toutes les devises
        self.c = currency_converter.CurrencyConverter()
        # On a une méthode pour définir les valeurs par defauts pour chaque ComboBox des devises
        self.set_default_values()
        # Méthode pour configurer les différentes connection sur les widgets
        self.setup_connections()

    # On fait une méthode pour englober les paramètres de l'ui qui serai établi pour l'interface
    def setup_ui(self):
        # Ici on définit une variable layout pour notre instance et de la façon Horizontal, on doit rajouter self
        # car cela appartiant à l'instance
        self.layout = QtWidgets.QHBoxLayout(self)
        # On ne met pas self car cela appartient au layout, et ce ceci est le widget pour spécifier la devise
        self.cbb_devisesFrom = QtWidgets.QComboBox()
        # On définit un widget pour y rentre le montant
        self.spn_montant = QtWidgets.QSpinBox()
        # On fais une box pour choisir la devise voulu
        self.cbb_devisesTo = QtWidgets.QComboBox()
        # On fait un widget pour le montant converti
        self.spn_montantConverti = QtWidgets.QSpinBox()
        # Et pour finir un bouton pour invervser les montants
        self.btn_inverser = QtWidgets.QPushButton("Inverser")

        # Voici la méthode pour ajouter les différents widgets que nous avons créer précdément
        self.layout.addWidget(self.cbb_devisesFrom)
        self.layout.addWidget(self.spn_montant)
        self.layout.addWidget(self.cbb_devisesTo)
        self.layout.addWidget(self.spn_montantConverti)
        self.layout.addWidget(self.btn_inverser)

    # Voici la méthode qui nous permettre de définir les valeurs par défaut
    def set_default_values(self):
        # Nous récupérons notre attributs qui correspond au widget de la devise, nous lui passons notre variable qui
        # contient les devises, mais comme ce n'est pas une liste on fait une conversion de type, puis on la trie
        # avec sorted
        self.cbb_devisesFrom.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesTo.addItems(sorted(list(self.c.currencies)))

        # Voici une méthode pour attribuer une valeur par défaut
        self.cbb_devisesFrom.setCurrentText("EUR")
        self.cbb_devisesTo.setCurrentText("EUR")

        # On fixe le minimum et le maximum
        self.spn_montant.setRange(1, 100000)
        self.spn_montantConverti.setRange(1, 100000)

        # Maintenant voici comment mettre les valeurs par défaut pour les SpinBox
        self.spn_montant.setValue(100)
        self.spn_montantConverti.setValue(100)

    # Voici notre méthode de configuration pour les connections
    def setup_connections(self):
        # Ceci fait la connection qui détecte le fait qu'on change la devise
        self.cbb_devisesFrom.activated.connect(self.compute)
        self.cbb_devisesTo.activated.connect(self.compute)

        # Des que le montant est touché on a la connection qui se fait
        self.spn_montant.valueChanged.connect(self.compute)

        # Des que le bouton est soumis alors la méthode est faite
        self.btn_inverser.clicked.connect(self.inverser_devise)

    # Voici la fonctionnement de la méthode pour le setup_css
    def setup_css(self):
        self.setStyleSheet("""
            background-color: rgb(30, 30, 30);
            color: rgb(240, 240, 240);
            border: none;
        """)

    # Cette méthode est appelé lors de la connection avec les spn et cbb
    def compute(self):
        # On donne des variables au valeur de nos champs
        montant = self.spn_montant.value()
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()

        # Pour corriger les erreurs qui pourrait arriver, on met un bloc try, donc ce qui se trouve dedans est lancé
        try:
            # On fait appel à self.c pour utiliser une méthode du module qui permet de faire la conversion avec tout
            # les calculs déjà implémenter, on donne la valeur à une variable
            resultat = self.c.convert(montant, devise_from, devise_to)
        # Si le bloc try rencontre une erreur on fait appel à except et vaut mieux toujours spécifié le type d'erreur
        except currency_converter.currency_converter.RateNotFoundError:
            print("La conversion n'as pas fonctionné")
        # Et du coup si il n'y a pas d'erreur, on effectue ce bloc
        else:
            # Ici on attribue du coup le spin du montant converti à la variable resultat
            self.spn_montantConverti.setValue(resultat)

    # La méthode qui va faire le transfer entre nos différentes devises
    def inverser_devise(self):
        # Nous récupérons les valeurs
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()

        # Les valeurs récupérées sont ensuite transmise au ComboBox inverse
        self.cbb_devisesFrom.setCurrentText(devise_to)
        self.cbb_devisesTo.setCurrentText(devise_from)

        # Ici on fait un rappel à la méthode compute pour nous éviter de copier coller le code de calcul
        self.compute()

# Ici on créer notre application, si nous oublions la parenthese et le fait d'initialiser une liste alors cela
# nous retourne une erreur
app = QtWidgets.QApplication([])

# Ici nous initialisons une feênetre pour notre application
win = App()

# Voici une méthode de notre instance pour montrer la fenêtre lors de l'exécution de l'app
win.show()

# Ici nous éxécutons notre application attention
app.exec_()