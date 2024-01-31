<template>
  <div id="app">
    <div class="bar">
      <div class="leftbar">
        <h1 style="font-family:'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;">Image Search App</h1>
      </div>
      <div class="rightbar">
        <img alt="Page logo" src="./assets/logo4.jpeg" style="width: 80px; height: auto;">
      </div>
    </div>
    <br>
      <input type="file" ref="fileInput" id="img" name="img" @change="RefreshImg" accept="image/*">
      <br><br>
      <button @click="displayImage" >Confirm Image</button>
      <img v-if="isImageLoaded" :src="selectedImage" alt="Selected Image" />
    <div v-if="ButtonPress">
      <img :src="selectedImage" alt="Selected Image" style="max-width: 300px; margin-top: 20px;">
      <br>
      <p>Similar Images:</p>
      <ul class="image-list">
      <li v-for="filename in searchResults" :key="filename">
        <img :src="getImageUrl(filename)" alt="Similar Image" class="similar-image" />
      </li>
    </ul>
    </div>
    <br><br><br><br><br>
    <div class="bottom-bar">
      <p>Universidad de los Andes</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedImage: null,
      isImageLoaded: false,
      ButtonPress: false,
      uploadedimage: false,
      searchResults: [],
    };
  },
  methods: {
    RefreshImg() {
      const fileInput = this.$refs.fileInput;
      const file = fileInput.files[0];

      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          this.selectedImage = reader.result;
          this.isImageLoaded = false;
          this.ButtonPress = false;
          this.searchResults = [];
        };
        reader.readAsDataURL(file);
      }
    },
    async displayImage() {
      if (this.selectedImage) {
        const formData = new FormData();
        const fileInput = this.$refs.fileInput;
        const file = fileInput.files[0];

        formData.append('file', file);
        this.ButtonPress = true;

        try {
          const response = await axios.post('http://localhost:8000/upload', formData);
          console.log('Image upload response:', response.data);
          this.uploadedimage = true;

          this.getSearchResults();
        } catch (error) {
          console.error('Error uploading image:', error);
        }
      }
    },
    async getSearchResults() {
      const queryPath = "uploaded_image.jpg";
      const datasetPath = "D:/TAREAS/App de busqueda/test";
      const device = "cuda";
      const nResults = 10; 

      try {
        const response = await axios.get(`http://localhost:8000/search?query_path=${queryPath}&dataset_path=${datasetPath}&device=${device}&n_results=${nResults}`);
        const results = response.data.results;
        console.log('Similar Images:', results);
        this.searchResults = results;
      } catch (error) {
        console.error('Error retrieving similar images:', error);
      }
    },
    getImageUrl(filename) {
      return `http://localhost:8000/similar_images/${filename}`;
    }
  },
};
</script>


<style>
body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  border: #2c3e50;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.bar {
  background-color: #78d3e9;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.leftbar {
  color: rgb(55, 76, 183);
}

.rightbar img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: #78d3e9;
  color: #2c3e50;
  padding: 5px;
  text-align: center;
}
.image-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
}

.similar-image {
  height: 200px;
  margin: 5px;
  object-fit: cover;
}
</style>