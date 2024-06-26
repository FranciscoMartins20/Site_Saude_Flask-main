document.getElementById('add_resultado').addEventListener('click', function() {
    var index = document.querySelectorAll('#resultados .resultado-item').length;
    var resultadosDiv = document.getElementById('resultados');
    var newResultado = `
        <div class="form-group resultado-item">
            <label for="resultados-${index}-area_examinada">Área Examinada</label><br>
            <input type="text" id="resultados-${index}-area_examinada" name="resultados-${index}-area_examinada" class="form-control">
            <label for="resultados-${index}-resultado">Resultado</label><br>
            <input type="text" id="resultados-${index}-resultado" name="resultados-${index}-resultado" class="form-control">
            <label for="resultados-${index}-observacoes">Observações</label><br>
            <input type="text" id="resultados-${index}-observacoes" name="resultados-${index}-observacoes" class="form-control">
            <button type="button" class="btn remove-resultado">Remover</button>
        </div>
    `;
    resultadosDiv.insertAdjacentHTML('beforeend', newResultado);
    attachRemoveHandlers();
});

function attachRemoveHandlers() {
    document.querySelectorAll('.remove-resultado').forEach(button => {
        button.removeEventListener('click', removeResultado);
        button.addEventListener('click', removeResultado);
    });
}

function removeResultado(event) {
    event.target.closest('.resultado-item').remove();
}

attachRemoveHandlers();
