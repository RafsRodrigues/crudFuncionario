$(function () {
    $(".btn-salvar").click(function () {
        var dados = [{
            "nome": $("#nome").val(),
            "data_nascimento": $("#data_nascimento").val(),
            "endereco": $("#endereco").val(),
            "telefone": $("#telefone").val()
        }];

        $.ajax({
            type: "POST",
            url: "/criar",
            data: JSON.stringify(dados),
            contentType: "application/json"
        })
            .done(function (resposta) {
                alert(resposta.mensagem);
                window.location.href = "/";
            })
            .fail(function (data) {
                alert(data.responseText);
            });

    });

    $(".btn-editar").click(function () {

        const dados = {
            id: $("#id").val(),
            nome: $("#nome").val(),
            data_nascimento: $("#data_nascimento").val(),
            endereco: $("#endereco").val(),
            telefone: $("#telefone").val()
        };

        $.ajax({
            type: "POST",
            url: "/atualizar",
            data: JSON.stringify(dados),
            contentType: "application/json"
        })
            .done(function (resposta) {
                alert(resposta.mensagem);
                window.location.href = "/";
            })
            .fail(function (data) {
                alert("Erro ao atualizar: " + data.responseText);
            });
    });
    
});


function confirmarDelecao(nome, url) {
    if (confirm(`Tem certeza que deseja deletar o funcionário ${nome}?`)) {
        window.location.href = url;
    }
}