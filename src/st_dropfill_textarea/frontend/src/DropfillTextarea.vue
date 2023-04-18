<template>
  <div class="container" :style="cssProps" ref="container">
    <div class="label" ref="label">
      {{ label }}
    </div>
    <div class="textarea-container" ref="textarea-container">
      <textarea
        ref="textarea"
        v-model="value"
        @change="handlesChange"
        @drop="handleDrop"
      />
    </div>
  </div>
</template>

<script>
  import { ref } from "vue";
  import { Streamlit } from "streamlit-component-lib";
  import { useStreamlit } from "./streamlit";
  import { convertToHtml } from "mammoth";

  export default {
    name: "DropfillTextarea",
    props: {
      args: Object,
    }, // Arguments that are passed to the plugin in Python are accessible in prop "args"
    setup() {
      useStreamlit(); // lifecycle hooks for automatic Streamlit resize
    },

    data() {
      const value = ref("");
      return {
        value,
      };
    },

    mounted() {
      this.value = ref(this.args.value);
      this.rerender();
    },

    computed: {
      label() {
        return this.args.label;
      },
      cssProps() {
        const propObj = {
          "--flex-direction": "column",
          "--margin-right": "0px",
          "--container-height": this.args.height * 1.15 + "px",
          "--textarea-height": this.args.height + "px",
          "--align-items": "left",
          "--background-color": "#f0f2f6",
        };
        if (this.args.layout !== "column") {
          propObj["--flex-direction"] = "row";
          propObj["--margin-right"] = "4px";
          propObj["--align-items"] = "center";
        }
        return propObj;
      },
    },

    methods: {
      renderColumn() {
        setTimeout(() => {
          const containerRef = this.$refs["container"];
          const labelRef = this.$refs["label"];
          const textareaRef = this.$refs["textarea"];
          const height = labelRef.clientHeight + textareaRef.clientHeight;
          const width = containerRef.clientWidth - 16 * 2 - 4;
          containerRef.style.height = height + "px";
          textareaRef.style.width = width + "px";
          textareaRef.style.height = this.args.height - 16 + "px";
        }, 500);
      },
      renderRow() {
        setTimeout(() => {
          const containerRef = this.$refs["container"];
          const labelRef = this.$refs["label"];
          const textareaContainerRef = this.$refs["textarea-container"];
          const textareaRef = this.$refs["textarea"];
          const labelWidth = this.args.labelWidth;
          let width;
          if (labelWidth !== null) {
            labelRef.style.width = labelWidth + "px";
            width = containerRef.clientWidth - labelWidth - 16 * 2 - 8;
          } else {
            width =
              containerRef.clientWidth - labelRef.clientWidth - 16 * 2 - 8;
          }
          const height = textareaContainerRef.clientHeight;

          containerRef.style.height = height + "px";
          textareaContainerRef.style.width = width + "px";
          textareaContainerRef.style.height = this.args.height + "px";
          textareaRef.style.height = this.args.height - 16 * 2 + "px";
        }, 500);
      },

      rerender() {
        if (this.args.layout === "column") {
          this.renderColumn();
        } else {
          this.renderRow();
        }
      },
      handlesChange() {
        Streamlit.setComponentValue(this.value);
      },

      updateValue(newValue) {
        this.value = newValue;
        this.handlesChange();
      },

      getTextFromNode(node) {
        let text = "";
        if (node.nodeType === Node.TEXT_NODE) {
          text += node.textContent.trim();
        } else {
          let children = [];
          for (const child of node.childNodes) {
            children.push(this.getTextFromNode(child));
          }
          children = children.filter((child) => child.length > 0);
          text += children.join("") + "\n";
        }
        return text;
      },

      convertToJson(html) {
        const parser = new DOMParser();
        const dom = parser.parseFromString(html, "text/html");
        const body = dom.getElementsByTagName("body")[0];
        const content = [];
        for (const node of body.childNodes) {
          const text = this.getTextFromNode(node);
          content.push(text);
        }
        let text = content.join("\n");
        text = text.replace(/(\r\n|\r|\n){2,}/g, "$1\n");
        this.updateValue(text);
      },

      handleDocx(file) {
        const reader = new FileReader();
        reader.onload = () => {
          convertToHtml({ arrayBuffer: reader.result }).then((result) => {
            this.convertToJson(result.value);
          });
        };

        reader.readAsArrayBuffer(file);
      },

      handleHtml(file) {
        const reader = new FileReader();
        reader.onload = () => {
          this.convertToJson(reader.result);
        };

        reader.readAsText(file);
      },

      handlPlainText(file) {
        const reader = new FileReader();
        reader.onload = () => {
          this.updateValue(reader.result);
        };

        reader.readAsText(file);
      },

      fileHandler(file) {
        const files = {
          "application/vnd.openxmlformats-officedocument.wordprocessingml.document": this
            .handleDocx,
          "text/html": this.handleHtml,
          "text/plain": this.handlPlainText,
        };
        return files[file.type];
      },

      handleDrop(event) {
        event.preventDefault();
        event.stopPropagation(); // stops the browser from redirecting.
        const file = event.dataTransfer.files[0];
        const handle = this.fileHandler(file);
        if (handle !== undefined) handle(file);
        else this.updateValue("Dropped file type not supported");
      },
    },
  };
</script>

<style scoped>
  .container {
    display: flex;
    flex-direction: var(--flex-direction);
    align-items: var(--align-items);
    height: var(--container-height);
  }
  .label {
    margin-right: var(--margin-right);
    font: var(--font);
    white-space: pre;
  }

  .textarea-container {
    width: 100%;
    display: flex;
    justify-content: center;
  }
  textarea {
    width: 100%;
    height: var(--textarea-height);
    resize: none;
    padding: 16px;
    border: none;
    border-radius: 6px;
    color: var(--text-color);
    background-color: var(--background-color);
    font: var(--font);
    scrollbar-width: none; /* hide the scrollbar when out of focus */
    overflow: hidden; /* hide the overflow when out of focus */
  }
  textarea:focus {
    outline: 1px solid red;
  }

  textarea:hover {
    scrollbar-width: auto; /* show the scrollbar when in focus */
    overflow: auto; /* show the overflow when in focus */
  }

  textarea::-webkit-scrollbar {
    width: 6px;
    height: 6px;
  }

  textarea::-webkit-scrollbar-thumb {
    border-radius: 100px;
    background-color: rgba(143, 141, 141, 0.8);
  }

  textarea::-webkit-scrollbar-track {
    border-radius: 100px;
  }
</style>
