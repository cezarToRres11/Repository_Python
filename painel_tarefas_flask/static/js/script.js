document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("darkModeBtn");

    function atualizarBotao() {
        if (!button) return;

        const escuro = document.body.classList.contains("dark-mode");

        button.innerHTML = escuro
            ? '<i class="bi bi-sun"></i> <span>Modo claro</span>'
            : '<i class="bi bi-moon-stars"></i> <span>Modo escuro</span>';
    }

    const salvo = localStorage.getItem("modoEscuro");

    if (salvo === "true") {
        document.body.classList.add("dark-mode");
    }

    atualizarBotao();

    if (button) {
        button.addEventListener("click", () => {
            document.body.classList.toggle("dark-mode");

            localStorage.setItem(
                "modoEscuro",
                document.body.classList.contains("dark-mode")
            );

            atualizarBotao();
        });
    }
});
