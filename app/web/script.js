        let index = 0;
        let total = 0;
        let baseImg = null;
        async function init() {
            const res = await fetch('/lndata');
            total = parseInt(await res.text());
            carregarImagem(index);
        }
        function addData() {
            const semantic = document.getElementById("semantic");
            const ctx = semantic.getContext("2d");
        
            // Converte o conteúdo do canvas para um formato base64 (dataURL)
            const imageData = semantic.toDataURL("image/png"); 
        
            // Envia a imagem (imageData) e o index para o backend
            fetch('/enviar-semantic', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    index: index,
                    imageData: imageData
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log("Dados enviados com sucesso:", data);
            })
            .catch(err => {
                console.error("Erro ao enviar dados:", err);
            });
        }
        function carregarImagem(n) {
            document.getElementById("semantic").style.opacity = "0";
            fetch(`/image/${n}?t=${Date.now()}`)
                .then(response => {
                    if (!response.ok) throw new Error("Imagem não encontrada");
                    return response.blob();
                })
                .then(blob => {
                    const url = URL.createObjectURL(blob);
                    const img = new Image();
                    img.onload = function () {
                        const canvas = document.getElementById("imagen");
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

        // function prever() {
        //     document.getElementById("loader").style.display = "block"; // Mostra o carregamento
        //     document.getElementById("semantic").style.opacity = "0.2";
        //     fetch(`/masc/${index}?t=${Date.now()}`)
        //         .then(response => {
        //             if (!response.ok) throw new Error("Máscara não encontrada");
        //             return response.blob();
        //         })
        //         .then(blob => {
        //             const url = URL.createObjectURL(blob);
        //             const mask = new Image();
        //             mask.onload = function () {
        //                 const canvas = document.getElementById("semantic");
        //                 const ctx = canvas.getContext("2d");

        //                 // Redesenha a imagem base antes de aplicar a máscara
        //                 if (baseImg) {
        //                     ctx.drawImage(baseImg, 0, 0, canvas.width, canvas.height);
        //                 }

        //                 // Cria uma camada de máscara
        //                 const maskCanvas = document.createElement("canvas");
        //                 maskCanvas.width = canvas.width;
        //                 maskCanvas.height = canvas.height;
        //                 const maskCtx = maskCanvas.getContext("2d");
        //                 maskCtx.drawImage(mask, 0, 0, canvas.width, canvas.height);

        //                 const imageData = maskCtx.getImageData(0, 0, canvas.width, canvas.height);
        //                 const data = imageData.data;

        //                 // Aplica a máscara com transparência
        //                 for (let i = 0; i < data.length; i += 4) {
        //                     const value = data[i]; // Assumindo que R = G = B
        //                     if (value === 1) {
        //                         // milho: verde
        //                         data[i] = 0;     // R
        //                         data[i + 1] = 255; // G
        //                         data[i + 2] = 0;   // B
        //                         data[i + 3] = 128; // A (transparência de 50%)
        //                     } else if (value === 2) {
        //                         // daninha: vermelho
        //                         data[i] = 255;
        //                         data[i + 1] = 0;
        //                         data[i + 2] = 0;
        //                         data[i + 3] = 128; // A (transparência de 50%)
        //                     } else {
        //                         // fundo (transparente)
        //                         data[i + 3] = 0;
        //                     }
        //                 }

        //                 // Aplica a máscara transparente na imagem
        //                 ctx.putImageData(imageData, 0, 0);
        //                 URL.revokeObjectURL(url);

        //                 // Esconde o carregamento
        //                 document.getElementById("loader").style.display = "none";
        //             };
        //             mask.src = url;
        //         })
        //         .catch(err => {
        //             alert(err.message);
        //             document.getElementById("loader").style.display = "none"; // Garante que some mesmo com erro
        //         });
        // }
        function prever() {
            document.getElementById("loader").style.display = "block";
            const canvas = document.getElementById("semantic");
            const ctx = canvas.getContext("2d");
        
            fetch(`/masc/${index}?t=${Date.now()}`)
                .then(response => {
                    if (!response.ok) throw new Error("Máscara não encontrada");
                    return response.blob();
                })
                .then(blob => {
                    const url = URL.createObjectURL(blob);
                    const img = new Image();
                    img.onload = function () {
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                        URL.revokeObjectURL(url);
        
                        // Aplica opacidade somente após a máscara estar visível
                        document.getElementById("semantic").style.opacity = "0.9";
                        document.getElementById("loader").style.display = "none";
                    };
                    img.src = url;
                })
                .catch(err => {
                    alert(err.message);
                    document.getElementById("loader").style.display = "none";
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