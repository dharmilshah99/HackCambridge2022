import { Streamlit, RenderData } from "streamlit-component-lib"

// Add text and a button to the DOM. (You could also add these directly
// to index.html.)
const span = document.body.appendChild(document.createElement("span"))
const textNode = span.appendChild(document.createTextNode(""))
const button = span.appendChild(document.createElement("button"))
button.textContent = "Start Recording"

// Add a click handler to our button. It will send data back to Streamlit.
let numClicks = 0
let isFocused = false
button.onclick = function (): void {
  // Increment numClicks, and pass the new value back to
  // Streamlit via `Streamlit.setComponentValue`.
  // numClicks += 1
  // Streamlit.setComponentValue(numClicks)
  navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
    console.log({ stream })
    if (!MediaRecorder.isTypeSupported('audio/webm'))
      return alert('Browser not supported')
    const mediaRecorder = new MediaRecorder(stream, {
      mimeType: 'audio/webm',
    })
    const socket = new WebSocket('wss://api.deepgram.com/v1/listen', [
      'token',
      '7e3ea4dfb0238df8ba87d72fc46ed37e19984beb',
    ])
    socket.onopen = () => {
      console.log({ event: 'onopen' })
      mediaRecorder.addEventListener('dataavailable', async (event) => {
        if (event.data.size > 0 && socket.readyState == 1) {
          socket.send(event.data)
        }
      })
      mediaRecorder.start(1000)
    }

    let liveFeed = ''
    socket.onmessage = (message) => {
      const received = JSON.parse(message.data)
      const transcript = received.channel.alternatives[0].transcript
      if (transcript && received.is_final) {
        console.log(transcript)
        liveFeed +=
          transcript + ' '
        Streamlit.setComponentValue(liveFeed)
      }
    }

    socket.onclose = () => {
      console.log({ event: 'onclose' })
    }

    socket.onerror = (error) => {
      console.log({ event: 'onerror', error })
    }
  })
}

button.onfocus = function (): void {
  isFocused = true
}

button.onblur = function (): void {
  isFocused = false
}

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event: Event): void {
  // Get the RenderData from the event
  const data = (event as CustomEvent<RenderData>).detail

  // Maintain compatibility with older versions of Streamlit that don't send
  // a theme object.
  if (data.theme) {
    // Use CSS vars to style our button border. Alternatively, the theme style
    // is defined in the data.theme object.
    const borderStyling = `1px solid var(${isFocused ? "--primary-color" : "gray"
      })`
    button.style.border = borderStyling
    button.style.outline = borderStyling
  }

  // Disable our button if necessary.
  button.disabled = data.disabled
}

// Attach our `onRender` handler to Streamlit's render event.
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)

// Tell Streamlit we're ready to start receiving data. We won't get our
// first RENDER_EVENT until we call this function.
Streamlit.setComponentReady()

// Finally, tell Streamlit to update our initial height. We omit the
// `height` parameter here to have it default to our scrollHeight.
Streamlit.setFrameHeight()
