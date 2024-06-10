document.addEventListener('DOMContentLoaded', function() {
    var pacientesDropdown = document.querySelector('select[name="paciente"]');
    var tipoExameField = document.querySelector('input[name="tipo_exame"]');
    var dataExameField = document.querySelector('input[name="data_exame"]');
    var descricaoField = document.querySelector('textarea[name="descricao"]');
    
    pacientesDropdown.addEventListener('change', function() {
        var userId = this.value;
        if (userId) {
            fetch('/api/user/' + userId + '/agendamentos')
                .then(response => response.json())
                .then(data => {
                    if (data.length > 0) {
                        tipoExameField.value = data[0].tipo;
                        dataExameField.value = data[0].data;
                        descricaoField.value = data[0].descricao;
                    } else {
                        tipoExameField.value = '';
                        dataExameField.value = '';
                        descricaoField.value = '';
                    }
                });
        } else {
            tipoExameField.value = '';
            dataExameField.value = '';
            descricaoField.value = '';
        }
    });

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
});
