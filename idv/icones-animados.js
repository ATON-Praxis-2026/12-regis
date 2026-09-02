/* ---------------------------------------------------------------------------
   Ícones animados da Regis, num lugar só.

   Os desenhos saíram de idv/icone-animado.html, que é a vitrine onde o time
   escolheu os cinco estudos. Este arquivo é o que a aplicação usa, e o par
   dele é idv/icones-animados.css. Mexer nos dois juntos.

   Como usar no HTML:

     <span data-icone="valvula" data-tam="20"></span>   roda em laço
     <span data-icone="cerebro" data-tam="28" data-uma></span>   toca uma vez

   E no JavaScript, quando o momento é que dispara:

     Regis.icones.criar("brilho", 14, true)   devolve o <svg> pronto
     Regis.icones.repetir(elemento)           toca de novo a versão de uma vez
     Regis.icones.congelar(elemento)          para no quadro pronto, sem repetir
     Regis.icones.montar(raiz)                acorda o que entrou na tela depois

   Cada estudo tem um significado e um lugar só, senão vira enfeite:
     valvula  estado de trabalho, onde a pessoa espera
     memoria  leitura acontecendo, a linha se escrevendo sozinha
     cerebro  conferi e guardei, confirmação sem palavra
     brilho   achei, o instante da descoberta
     registro o vazamento, e por isso só antes de conectar a conta
   --------------------------------------------------------------------------- */
(function (global) {
  "use strict";

  var MOEDA = "<g class=\"moeda mN\"><g transform=\"translate(644.4,-126.4) scale(.22)\"><path class=\"dinheiro\" d=\"M444-200h70v-50q50-9 86-39t36-89q0-42-24-77t-96-61q-60-20-83-35t-23-41q0-26 18.5-41t53.5-15q32 0 50 15.5t26 38.5l64-26q-11-35-40.5-61T516-710v-50h-70v50q-50 11-78 44t-28 74q0 47 27.5 76t86.5 50q63 23 87.5 41t24.5 47q0 33-23.5 48.5T486-314q-33 0-58.5-20.5T390-396l-66 26q14 48 43.5 77.5T444-252v52Zm36 120q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Z\"/></g></g>";

  var CORPO = {
    valvula: "<path d=\"M160-120v-320h80v40h120v-120h-40v-80h320v80h-40v120h120v-40h80v320h-80v-40H240v40h-80Zm80-120h480v-80H520v-200h-80v200H240v80Zm240 0Z\"/><path d=\"M440-760h80v120h-80z\"/><path class=\"alavanca\" d=\"M280-840h400v80H280z\"/>",
    memoria: "<path d=\"M240-80q-50 0-85-35t-35-85v-120h120v-560l60 60 60-60 60 60 60-60 60 60 60-60 60 60 60-60 60 60 60-60v680q0 50-35 85t-85 35H240Zm480-80q17 0 28.5-11.5T760-200v-560H320v440h360v120q0 17 11.5 28.5T720-160ZM240-160h360v-80H200v40q0 17 11.5 28.5T240-160Zm-40 0v-80 80Z\"/><path class=\"linha l1\" d=\"M360-680h240v80H360Z\"/><path class=\"ponto p1 dinheiro\" d=\"M680-600q-17 0-28.5-11.5T640-640q0-17 11.5-28.5T680-680q17 0 28.5 11.5T720-640q0 17-11.5 28.5T680-600Z\"/><path class=\"linha l2\" d=\"M360-560h240v80H360Z\"/><path class=\"ponto p2 dinheiro\" d=\"M680-480q-17 0-28.5-11.5T640-520q0-17 11.5-28.5T680-560q17 0 28.5 11.5T720-520q0 17-11.5 28.5T680-480Z\"/>",
    cerebro: "<path class=\"cabeca\" d=\"M240-80v-172q-57-52-88.5-121.5T120-520q0-150 105-255t255-105q125 0 221.5 73.5T827-615l52 205q5 19-7 34.5T840-360h-80v120q0 33-23.5 56.5T680-160h-80v80h-80v-160h160v-200h108l-38-155q-23-91-98-148t-172-57q-116 0-198 81t-82 197q0 60 24.5 114t69.5 96l26 24v208h-80Zm254-360Z\"/><path class=\"marca\" d=\"M365-520.7 442.1-443.6 595-596.5\"/>",
    brilho: "<path class=\"cabeca\" d=\"M240-80v-172q-57-52-88.5-121.5T120-520q0-150 105-255t255-105q125 0 221.5 73.5T827-615l52 205q5 19-7 34.5T840-360h-80v120q0 33-23.5 56.5T680-160h-80v80h-80v-160h160v-200h108l-38-155q-23-91-98-148t-172-57q-116 0-198 81t-82 197q0 60 24.5 114t69.5 96l26 24v208h-80Zm254-360Z\"/><g class=\"faisca f0\"><g transform=\"translate(322.5,-310) scale(.4375)\"><path d=\"M360-160L260-380L40-480L260-580L360-800L460-580L680-480L460-380Z\"/></g></g><g class=\"faisca f1\"><g transform=\"translate(565,-580) scale(.125)\"><path d=\"M360-160L260-380L40-480L260-580L360-800L460-580L680-480L460-380Z\"/></g></g><g class=\"faisca f2\"><g transform=\"translate(330.6,-347.5) scale(.109)\"><path d=\"M360-160L260-380L40-480L260-580L360-800L460-580L680-480L460-380Z\"/></g></g>",
    registro: "<g transform=\"translate(30.8,-409.2) scale(.62)\"><path d=\"M160-120v-320h80v40h120v-120h-40v-80h320v80h-40v120h120v-40h80v320h-80v-40H240v40h-80Zm80-120h480v-80H520v-200h-80v200H240v80Zm240 0Z\"/><path d=\"M440-760h80v120h-80z\"/><path class=\"alavanca\" d=\"M280-840h400v80H280z\"/></g><path class=\"bica\" d=\"M527-632.6H620a179.6 179.6 0 0 1 179.6 179.6V-320\"/><path class=\"bica\" d=\"M527-533.4H620a80.4 80.4 0 0 1 80.4 80.4V-320\"/>"
      + MOEDA.replace("mN", "m1")
      + MOEDA.replace("mN", "m2")
      + MOEDA.replace("mN", "m3")
  };

  function criar(nome, tam, uma) {
    var corpo = CORPO[nome];
    if (!corpo) return null;
    var t = tam || 24;
    var classe = "ri ri-" + nome + (uma ? " ri-uma" : "");
    var caixa = document.createElement("div");
    caixa.innerHTML =
      '<svg class="' + classe + '" viewBox="0 -960 960 960" width="' + t + '" height="' + t +
      '" aria-hidden="true" focusable="false">' + corpo + "</svg>";
    return caixa.firstChild;
  }

  /* Tocar de novo: a animação de uma vez só reinicia se a classe sair e
     voltar, e o navegador só percebe se ele for obrigado a recalcular no
     meio. É o que o offsetWidth faz aqui, não é sobra. */
  function repetir(el) {
    if (!el) return;
    var svg = el.classList && el.classList.contains("ri") ? el : el.querySelector(".ri");
    if (!svg) return;
    svg.classList.remove("ri-uma");
    void svg.offsetWidth;
    svg.classList.add("ri-uma");
  }

  /* Congelar: o desenho para no quadro em que a coisa aconteceu e não volta a
     acontecer. É o que a tela usa quando a pessoa revisita algo já visto. */
  function congelar(el) {
    if (!el) return;
    var svg = el.classList && el.classList.contains("ri") ? el : el.querySelector(".ri");
    if (!svg) return;
    svg.classList.remove("ri-uma");
    svg.classList.add("ri-fim");
  }

  function montar(raiz) {
    var alvos = (raiz || document).querySelectorAll("[data-icone]");
    for (var i = 0; i < alvos.length; i++) {
      var slot = alvos[i];
      if (slot.firstElementChild) continue;
      var svg = criar(slot.dataset.icone, slot.dataset.tam, slot.hasAttribute("data-uma"));
      if (svg) slot.appendChild(svg);
    }
  }

  global.Regis = global.Regis || {};
  global.Regis.icones = { criar: criar, repetir: repetir, congelar: congelar, montar: montar };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { montar(); });
  } else {
    montar();
  }
})(window);
