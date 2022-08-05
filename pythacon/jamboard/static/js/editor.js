let editor;

editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.session.setMode("ace/mode/c_cpp");
document.addEventListener("keyup", () => {
  if (editor.isFocused()) {
    let code = editor.getValue();
    chatSocket.send(
      JSON.stringify({
        type: "edit",
        data: code,
      })
    );
  }
});

function changeLanguage() {
  let language = document.querySelector("#languages").value;

  if (language == "c" || language == "cpp")
    editor.session.setMode("ace/mode/c_cpp");
  else if (language == "java") editor.session.setMode("ace/mode/java");
  else if (language == "python") editor.session.setMode("ace/mode/python");
  else if (language == "node") editor.session.setMode("ace/mode/javascript");

  chatSocket.send(JSON.stringify({type:"lang-change",lang:language}));
}

function changeLang(data){
    let language=data.lang;
    
    if (language == "c" || language == "cpp")
      editor.session.setMode("ace/mode/c_cpp");
    else if (language == "java") editor.session.setMode("ace/mode/java");
    else if (language == "python") editor.session.setMode("ace/mode/python");
    else if (language == "node") editor.session.setMode("ace/mode/javascript");

    document.querySelector("#languages").value=language;
}

function changeTheme() {
  let theme = document.querySelector("#themes").value;

  if (theme == "monokai") editor.setTheme("ace/theme/monokai");
  else if (theme == "chrome") editor.setTheme("ace/theme/chrome");
}

function editText(data) {
  editor.setValue(data.data||'');
}
