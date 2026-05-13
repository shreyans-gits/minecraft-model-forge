## Project Status: Archived / Proof of Concept
This project was an exploration into fine-tuning TinyLlama-1.1B for Minecraft 3D geometry generation.

### Results:
- ✅ **Success:** Successfully trained the model to follow the Minecraft JSON schema (loss reduced to 0.19).
- ✅ **Success:** Achieved high-fidelity generation for "Campfire" blocks with valid UV mapping.
- ⚠️ **Limitation:** The 1.1B model demonstrates strong pattern memorization but lacks the spatial reasoning to generalize to unobserved shapes (e.g., doors, tables) without a larger, more diverse dataset.

### Technical Takeaways:
- Small LLMs are highly sensitive to "spatial drift" in coordinate systems.
- "Deep Seeding" is required to anchor the model to 3D world boundaries (0-16 grid).
- Defensive JSON parsing is necessary to handle syntax jitter in low-parameter models.