document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("lessonForm");
  if (!form) return;
  const logoFile = document.getElementById("logoFile");
  const logoData = document.getElementById("logoData");
  if (logoFile && logoData) {
    logoFile.addEventListener("change", () => {
      const file = logoFile.files && logoFile.files[0];
      if (!file) return;
      if (file.size > 1024 * 1024) { alert("Please choose a logo smaller than 1 MB."); logoFile.value = ""; return; }
      const reader = new FileReader();
      reader.onload = () => { logoData.value = String(reader.result || ""); };
      reader.readAsDataURL(file);
    });
  }
  form.addEventListener("submit", (event) => {
    const objectives = [...form.querySelectorAll('input[name^="objective_"]')].filter(x => !x.name.startsWith("objective_verb_"));
    if (!objectives.some(x => x.value.trim())) {
      event.preventDefault();
      alert("Please enter at least one learning objective.");
      return;
    }
  });
});