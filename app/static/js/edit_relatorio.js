document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('add_resultado').addEventListener('click', function() {
        const resultados = document.getElementById('resultados');
        const resultadoItem = document.createElement('div');
        resultadoItem.className = 'resultado-item';

        resultadoItem.innerHTML = `
            <div class="form-group">
                <label for="area_examinada">Área Examinada</label>
                <input type="text" name="area_examinada" class="form-control">
            </div>
            <div class="form-group">
                <label for="resultado">Resultado</label>
                <input type="text" name="resultado" class="form-control">
            </div>
            <div class="form-group">
                <label for="observacoes">Observações</label>
                <input type="text" name="observacoes" class="form-control">
            </div>
            <button type="button" class="btn remove-resultado">Remover</button>
        `;

        resultados.appendChild(resultadoItem);

        resultadoItem.querySelector('.remove-resultado').addEventListener('click', function() {
            resultados.removeChild(resultadoItem);
        });
    });

    document.querySelectorAll('.remove-resultado').forEach(button => {
        button.addEventListener('click', function() {
            button.closest('.resultado-item').remove();
        });
    });

    document.getElementById('imagem_url').addEventListener('change', function(event) {
        const input = event.target;
        const reader = new FileReader();

        reader.onload = function() {
            const dataURL = reader.result;
            const previewImage = document.getElementById('new_imagem_preview');
            previewImage.src = dataURL;
            previewImage.style.display = 'block';
        };

        reader.readAsDataURL(input.files[0]);
    });
});
