import flet as ft

def mainPage(pagina):
  texto = ft.Text('Chatzone')

  chat = ft.Column()

  nome_usuario = ft.TextField(label='Escreva seu nome aqui')

  def enviarMsgTunel(mensagem):
    tipo = mensagem['tipo']
    if tipo == 'mensagem':
      textoMsg = mensagem['texto']
      usuarioMsg = mensagem['usuario']
      chat.controls.append(ft.Text(f'{usuarioMsg}: {textoMsg}'))
      pagina.update()
    else:
      usuarioMsg = mensagem['usuario']
      chat.controls.append(ft.Text(f'{usuarioMsg} entrou no chat', size=12, color=ft.colors.AMBER_400, italic=True))
      pagina.update()


  pagina.pubsub.subscribe(enviarMsgTunel)

  def enviarMsg(e):
    pagina.pubsub.send_all({
      'texto': campo_msg.value,
      'usuario': nome_usuario.value,
      'tipo': 'mensagem'
      })
    campo_msg.value =''
    pagina.update()

  campo_msg = ft.TextField(label='Digite uma mensagem', on_submit=enviarMsg)
  botao_enviar_msg = ft.ElevatedButton('Enviar', on_click=enviarMsg)



  def entrarPopup(e):
    pagina.pubsub.send_all({'usuario': nome_usuario.value, 'tipo': 'entrada'})
    pagina.add(chat)
    popup.open=False
    pagina.remove(botao_iniciar)
    pagina.add(ft.Row([
      campo_msg,
      botao_enviar_msg
    ]))
    pagina.update()

  popup = ft.AlertDialog(
    open=False,
    modal=True,
    title=ft.Text('Bem vindo ao Chatzone'),
    content=nome_usuario,
    actions=[
      ft.ElevatedButton('Entrar', on_click=entrarPopup)
    ],
  )

  def entrarChat(e):
    pagina.dialog = popup
    popup.open = True
    pagina.update()

  botao_iniciar = ft.ElevatedButton('Iniciar Chat', on_click=entrarChat)


  pagina.add(texto)
  pagina.add(botao_iniciar)

ft.app(target=mainPage, view=ft.WEB_BROWSER, port=8000)