document.getElementById('add_resultado').addEventListener('click', function() {
    var index = document.querySelectorAll('#resultados .form-group').length / 3;
    var resultadosDiv = document.getElementById('resultados');
    var newResultado = `
        <div class="form-group">
            <label for="resultados-${index}-area_examinada">Área Examinada</label><br>
            <input type="text" id="resultados-${index}-area_examinada" name="resultados-${index}-area_examinada" class="form-control">
        </div>
        <div class="form-group">
            <label for="resultados-${index}-resultado">Resultado</label><br>
            <input type="text" id="resultados-${index}-resultado" name="resultados-${index}-resultado" class="form-control">
        </div>
        <div class="form-group">
            <label for="resultados-${index}-observacoes">Observações</label><br>
            <input type="text" id="resultados-${index}-observacoes" name="resultados-${index}-observacoes" class="form-control">
        </div>
    `;
    resultadosDiv.insertAdjacentHTML('beforeend', newResultado);
});
