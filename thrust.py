import numpy as np
import matplotlib.pyplot as plt

# Constantes du moteur et de l'environnement
k = 1.4  # Coefficient de chaleur spécifique
R = 8.3145  # Constante universelle des gaz parfaits en J/(mol·K)

# Spécifications de la chambre de combustion
Tcc = 3455  # Température en K
rhocc = 2.4746  # Masse volumique en kg/m^3

# Paramètres géométriques de la tuyère
ycol = 73.41  # Rayon au col de la tuyère en mm
Acol = np.pi * (ycol ** 2)  # Aire de la section au col
Epsi = 117  # Rapport de section
ysor = np.sqrt(ycol**2 * Epsi)  # Rayon de sortie de la tuyère
L = 2150  # Longueur de la tuyère en mm
ini_teta = [60, 11, 8.5]  # Angles d'inclinaison initiaux

# Initialisation des vecteurs de calcul
x = np.linspace(0, L, 1000)  # Vecteur de positions le long de la tuyère
n_values = np.arange(2.3, 2.6, 0.1)  # Valeurs de l'exposant n
teta = np.full(len(x), ini_teta[1])  # Initialisation des angles
n_teta = np.ones(len(x))  # Initialisation du profil teta

# Définition des segments de teta en fonction de la position dans la tuyère
teta[x < 0.6 * L] = ini_teta[0]
teta[x == L] = ini_teta[2]
n_teta[x < 0.6 * L] = 0.5
n_teta[x == L] = 2

# Initialisation pour stocker les profils y
y_profiles = np.zeros((len(x), len(n_values) + 4))

# Calcul des profils de rayon pour chaque valeur de n
for j, n in enumerate(n_values):
    y_profiles[:, j] = ycol + (ysor - ycol) * (x / L)**n

# Calcul des autres profils
y_profiles[:, len(n_values)] = ycol * np.exp((x / L) * np.log(ysor / ycol))  # Profil exponentiel
y_profiles[:, len(n_values) + 1] = ycol + (ysor - ycol) * (x / L)**2 * (1 - np.cos(np.radians(90)))  # Profil cosinus
y_profiles[:, len(n_values) + 2] = ycol + (ysor - ycol) * (x / L)  # Profil linéaire
y_profiles[:, len(n_values) + 3] = ycol * np.exp((x / L) * np.log(ysor / ycol))  # Profil logarithmique

#Profil retenu
y = y_profiles[:, 0]


# Tracé des courbes pour chaque profil
plt.figure()
for j, n in enumerate(n_values):
    plt.plot(x, y_profiles[:, j], linewidth=2, label=f'n = {n}')
plt.plot(x, y_profiles[:, len(n_values)], linewidth=2, label='Exponentiel')
plt.plot(x, y_profiles[:, len(n_values) + 1], linewidth=2, label='Cosinus')
plt.plot(x, y_profiles[:, len(n_values) + 2], linewidth=2, label='Linéaire')
plt.plot(x, y_profiles[:, len(n_values) + 3], linewidth=2, label='Logarithmique')
plt.xlabel('Longueur (x)')
plt.ylabel('Rayon (y)')
plt.title('Différents Profils pour une Tuyère')
plt.legend()
plt.grid(True)
plt.show()

# Tracé du profil retenu symétriquement
plt.figure()
plt.plot(x, y, linewidth=2, label='Profil retenu')
plt.plot(x, -y, linewidth=2)  # Symétrie pour visualisation
plt.xlabel('Longueur (x)')
plt.ylabel('Rayon (y)')
plt.title('Profil retenu')
plt.legend()
plt.grid(True)
plt.show()

# Calcul des paramètres d'écoulement : aire, nombre de Mach, température et masse volumique
A = np.pi * y**2  # Aire en fonction de la position
Mx = (((1.728 * A / Acol) - 1)**(1 / 3)) / np.sqrt((k - 1) / k)  # Nombre de Mach
T = Tcc / (1 + ((k - 1) / 2) * Mx**2)  # Température
rho = rhocc / ((1 + ((k - 1) / 2) * Mx**2)**(1 / (k - 1)))  # Masse volumique

# Tracés des courbes de température, nombre de Mach et masse volumique
figures_data = [
    (T, 'Température', 'K°'),
    (Mx, 'Nombre de Mach', 'M'),
    (rho, 'Masse volumique', 'kg/m^3')
]

for data, title, ylabel in figures_data:
    plt.figure()
    plt.plot(x, data, linewidth=2, label=title)
    plt.xlabel('Longueur (x)')
    plt.ylabel(ylabel)
    plt.title(f'Évolution de {title.lower()} le long de la tuyère')
    plt.legend()
    plt.grid(True)
    plt.show()