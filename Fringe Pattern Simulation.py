import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider

def plot_interactive_fringes(
    Coherence = 1.0,         # Degree of coherence (0 to 1)
    Intensity1 = 1.0,        # Intensity of reference wave
    Intensity2 = 1.0,        # Intensity of object wave
    thetaDeg = 10            # Angle propagation of the two waves
):
    wavelength = 532e-9 # in meters
    theta = np.deg2rad(thetaDeg) # Angle of propagation into radians
    pixelSize = 1e-6  # Pixel size in meters
    width = 1000  # Number of pixels in x-direction
    height = 1000 # Number of pixels in x-direction


    # 2D Grid
    x = np.linspace(-width / 2 * pixelSize, width / 2 * pixelSize, width)
    y = np.linspace(-height / 2 * pixelSize, height / 2 * pixelSize, height)
    X, Y = np.meshgrid(x, y) # Function to hold the coordinates

    k = 2 * np.pi / wavelength # Wave number
    deltaPhi = k * 2 * np.sin(theta/2) * X # Phase differnece of the two wavelengths

    IdealIntensity = Intensity1 + Intensity2 + 2 * np.sqrt(Intensity1 * Intensity2) * np.cos(deltaPhi) * Coherence # Intenstiy of the intefernce of the two sources

    sigma = 80e-6  # Adjust: 50–120 µm typical for moderate vignette
    GaussianEnvelope = np.exp( - (X**2 + Y**2) / (2 * sigma**2) )

    Intensity = IdealIntensity * GaussianEnvelope # Intensity of the interference pattern

    Visibility = (2 * np.sqrt(Intensity1 * Intensity2) * Coherence) / (Intensity1 + Intensity2) # Visibility of Fringes

    Intensity = (Intensity - Intensity.min()) / (Intensity.max() - Intensity.min()) # Normalize intensity to [0, 1] for grayscale display

    # Plotting and and creating an image of the Fringe Patterns
    plt.figure(figsize=(8, 8))  # Set figure size
    plt.imshow(Intensity, cmap='gray', extent=[x.min(), x.max(), y.min(), y.max()])
    plt.title(f"Interactive Linear Fringe Pattern\n(Coherence={Coherence:.2f}, I1={Intensity1:.2f}, I2={Intensity2:.2f}, θ={thetaDeg:.1f}°, Vis={Visibility:.1f})")
    plt.xlabel("x (meters)")
    plt.ylabel("y (meters)")
    plt.colorbar(label="Normalized Intensity")
    plt.xlim([-0.000005, 0.000005]) # Zoom in on the x-axis
    plt.ylim([-0.000005, 0.000005]) # Zoom in on the y-axis
    plt.show()

interact(
    plot_interactive_fringes,
    Coherence=FloatSlider(min=0.0, max=1.0, step=0.05, value=1.0, description="Coherence"),
    Intensity1=FloatSlider(min=0.1, max=2.0, step=0.1, value=1.0, description="Intensity1 (Ref)"),
    Intensity2=FloatSlider(min=0.1, max=2.0, step=0.1, value=1.0, description="Intensity2 (Obj)"),
    thetaDeg=FloatSlider(min=0, max=20.0, step=0.5, value=10.0, description="θ (deg)")
)
