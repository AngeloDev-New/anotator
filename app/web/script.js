let index = 0;
        let total = 0;
        let baseImg = null;

        async function init() {
            const res = await fetch('/lndata');
            total = parseInt(await res.text());
            carregarImagem(index);
        }

        function carregarImagem(n) {
            fetch(`/image/${n}?t=${Date.now()}`)
                .then(response => {
                    if (!response.ok) throw new Error("Imagem não encontrada");
                    return response.blob();
                })
                .then(blob => {
                    const url = URL.createObjectURL(blob);
                    const img = new Image();
                    img.onload = function () {
                        const canvas = document.getElementById("canvas");
                        const ctx = canvas.getContext("2d");
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                        baseImg = img;
                        URL.revokeObjectURL(url);
                    };
                    img.src = url;
                })
                .catch(err => {
                    alert(err.message);
                });
        }

        function prever() {
            document.getElementById("loader").style.display = "block"; // Mostra o carregamento

            fetch(`/masc/${index}?t=${Date.now()}`)
                .then(response => {
                    if (!response.ok) throw new Error("Máscara não encontrada");
                    return response.blob();
                })
                .then(blob => {
                    const url = URL.createObjectURL(blob);
                    const mask = new Image();
                    mask.onload = function () {
                        const canvas = document.getElementById("canvas");
                        const ctx = canvas.getContext("2d");

                        // Redesenha a imagem base antes de aplicar a máscara
                        if (baseImg) {
                            ctx.drawImage(baseImg, 0, 0, canvas.width, canvas.height);
                        }

                        // Cria uma camada de máscara
                        const maskCanvas = document.createElement("canvas");
                        maskCanvas.width = canvas.width;
                        maskCanvas.height = canvas.height;
                        const maskCtx = maskCanvas.getContext("2d");
                        maskCtx.drawImage(mask, 0, 0, canvas.width, canvas.height);

                        const imageData = maskCtx.getImageData(0, 0, canvas.width, canvas.height);
                        const data = imageData.data;

                        // Aplica a máscara com transparência
                        for (let i = 0; i < data.length; i += 4) {
                            const value = data[i]; // Assumindo que R = G = B
                            if (value === 1) {
                                // milho: verde
                                data[i] = 0;     // R
                                data[i + 1] = 255; // G
                                data[i + 2] = 0;   // B
                                data[i + 3] = 128; // A (transparência de 50%)
                            } else if (value === 2) {
                                // daninha: vermelho
                                data[i] = 255;
                                data[i + 1] = 0;
                                data[i + 2] = 0;
                                data[i + 3] = 128; // A (transparência de 50%)
                            } else {
                                // fundo (transparente)
                                data[i + 3] = 0;
                            }
                        }

                        // Aplica a máscara transparente na imagem
                        ctx.putImageData(imageData, 0, 0);
                        URL.revokeObjectURL(url);

                        // Esconde o carregamento
                        document.getElementById("loader").style.display = "none";
                    };
                    mask.src = url;
                })
                .catch(err => {
                    alert(err.message);
                    document.getElementById("loader").style.display = "none"; // Garante que some mesmo com erro
                });
        }

        function proxima() {
            index = (index + 1) % total;
            carregarImagem(index);
        }

        function anterior() {
            index = (index - 1 + total) % total;
            carregarImagem(index);
        }

        window.onload = init;