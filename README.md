# Learning Manim for Physics 🎬🔬

Welcome to this repository dedicated to learning **Manim** (Mathematical Animation Engine) applied to physics. Here you'll find practical examples and visualizations of fundamental physics concepts.

## 📚 Repository Contents

This repository contains animations and visualizations of various physics topics, each with complete source code and a visual demonstration.

---

## 🌌 Available Visualizations

### 1. Spacetime Deformation (with Star)
**File**: `sun_space-time18.md` `space-time18.md`  

3D visualization of how a massive object deforms spacetime around it, similar to the effect of a black hole. Features an animated central star with solar corona and pulsating flames.

**Main Features:**
- Deformable grid simulating spacetime curvature
- Central star with multiple glow layers
- Solar corona animation with dynamic flames
- Geodesic showing how trajectories curve
- Cinematic 3D camera movements

**Demo:**

https://github.com/user-attachments/assets/f480ce53-9b55-4725-9176-7928b5601a72


**Physical Concepts:**
- Einstein's General Relativity
- Spacetime curvature
- Schwarzschild radius
- Geodesics in non-Euclidean geometry

---

### 2. Spacetime Deformation (Simplified Version)
**File**: `Space-time18.md`

A lighter version of the previous visualization, focused on fundamental concepts without the additional star animations.

**Main Features:**
- Deformable grid with dynamic shadows
- Central singularity represented by a green point
- Two reference radii (Schwarzschild and outer)
- Visualization of distances in curved vs. flat space
- Smooth transition from flat to curved space

**Demo:**

https://github.com/user-attachments/assets/21826bba-2583-42c9-8a7c-c5e2682c7550 

**Physical Concepts:**
- Spacetime curvature
- Difference between Euclidean and curved distances
- Gravitational effect on geometry

---

## 🚀 How to Use This Repository

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Manim Community** installed. To install it:
   ```bash
   pip install manim
   ```
3. **FFmpeg** for video rendering (Manim uses it internally)

### Running the Animations

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/manim-physics.git
   cd manim-physics
   ```

2. Navigate to the folder of the example you want to run

3. Extract the Python code from the corresponding `.md` file

4. Run the script with Manim:
   ```bash
   manim -pql your_file.py SpacetimeDeformation
   ```

   Quality options:
   - `-ql`: Low quality (fast for testing)
   - `-qm`: Medium quality
   - `-qh`: High quality
   - `-qk`: 4K quality (maximum quality, slower)
   - `-p`: Automatically play after rendering

### File Structure

Each `.md` file contains:
- 📝 **Complete Python code** with explanatory comments
- 🎥 **Visual demonstration** (GIF or video)
- 📖 **Detailed explanation** of physical concepts
- 🔧 **Technical details** of the implementation

---

## 📖 Resources for Learning Manim

### Official Documentation
- [Manim Community Docs](https://docs.manim.community/)
- [Example Gallery](https://docs.manim.community/en/stable/examples.html)

### Recommended Tutorials
- [3Blue1Brown](https://www.youtube.com/c/3blue1brown) - The original creator of Manim
- [Theorem of Beethoven](https://www.youtube.com/c/TheoremofBeethoven) - Manim tutorials

### Community
- [Manim Discord](https://discord.gg/manim)
- [Reddit r/manim](https://www.reddit.com/r/manim/)

---

## 🎯 Learning Objectives

With this repository you will learn to:

1. **Create 3D visualizations** of complex physics concepts
2. **Animate mathematical objects** like functions, curves, and surfaces
3. **Implement dynamic deformations** of space
4. **Control the camera** in 3D scenes
5. **Use updaters** for continuous animations
6. **Optimize rendering** of complex scenes
7. **Apply physics principles** in educational animations

---

## 🤝 Contributions

Contributions are welcome! If you have a physics visualization you'd like to add:

1. Fork the repository
2. Create a branch with your new visualization (`git checkout -b feature/new-visualization`)
3. Add your code in a `.md` file with complete explanation
4. Commit your changes (`git commit -m 'Add visualization of X'`)
5. Push to the branch (`git push origin feature/new-visualization`)
6. Open a Pull Request

### Format for Contributions

Each new visualization should include:
- Complete and commented Python code
- Explanation of physical concepts
- Visual demonstration (GIF or video)
- Bibliographic references if applicable

---

## 📝 Planned Future Topics

- ⚡ Electromagnetic fields and field lines
- 🌊 Mechanical waves and superposition
- 🔄 Simple harmonic motion
- 🎯 Elastic and inelastic collisions
- 🌀 Angular momentum and torque
- 🔬 Quantum tunneling effect
- 🌡️ Thermodynamics and entropy
- 🔭 Planetary orbits and Kepler's laws

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## 👨‍💻 Author

Created with ❤️ to facilitate physics learning through interactive visualizations.

---

## ⭐ Acknowledgments

- To the **Manim** community for this incredible tool
- To **3Blue1Brown** for inspiring this type of visualization
- To all physicists and educators who make science more accessible

---

## 📞 Contact

If you have questions, suggestions, or find any errors, feel free to:
- Open an **Issue** in this repository
- Contact me directly

---

**Happy learning and visualizing! 🚀📚**
