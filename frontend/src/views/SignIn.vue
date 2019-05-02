<template>
    <div class="page">
      <div class="wrapper fadeInDown">
        <div id="formContent">
          <h4 v-if="!pictureTaken">Please center your face</h4>
          <div>
            <vc-cam ref="camera" fit="cover" ></vc-cam>
          </div>
          <form @submit.prevent="login(true)">
            <input v-model="name" type="name" id="name" v-bind:class="{ 'fadeIn second notValid': $v.name.$invalid, 'fadeIn second valid': !$v.name.$invalid }" name="name" placeholder="Name">
            <button v-bind:disabled="$v.name.$invalid || !pictureTaken" type="submit"  class="fadeIn btn btn-primary" >Login</button>
          </form>
          <div class="mt-3">
            <input  type="file" name="embedding" @change="uploadFile($event)" accept=".dat" class="fadeIn input-file">
            <button v-on:click="login(false)" v-bind:disabled="$v.name.$invalid || embedding === null" type="submit" class="fadeIn btn btn-info">Login using Embedding</button>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
  import { required } from "vuelidate/lib/validators";
  export default {
    name: 'login',
    data() {
      return {
        name: '',
        size: 300,
        loader: null,
        embedding: null,
        face: null,
        picture: '',
        pictureTaken: false
      }
    },
    validations: {
      name: { required }
    },
    methods: {
      spinner(){
        this.loader = this.$loading.show({
          canCancel: true,
          onCancel: this.onCancel,
        });
      },
      cancelLoader(){
        this.loader.hide();
      },
      login(imageFlag){
        this.spinner();
        this.$v.name.$touch();
        if(this.$v.name.$error) return;
        this.name = this.name.toLowerCase();
        this.$http.post('https://smith-face-login.herokuapp.com/login', imageFlag ? { 
            name: this.name, 
            image: this.picture, 
            imageFlag: imageFlag 
          }: { 
            name: this.name, 
            embedding: JSON.parse(this.embedding), 
            imageFlag: imageFlag 
          }).then(response => {
          console.log("response", response);
          this.$swal({
            type: 'success',
            title: 'Logged In'
          });
          this.cancelLoader();
        }, err => {
          console.log("err", err)
          this.cancelLoader();
          if (err.status === 403){
            this.$swal({
              type: 'error',
              title: 'Oops...',
              text: 'Name doesn\'t match your face'
            });
          }else if (err.status === 400){
            this.$swal({
              type: 'error',
              title: 'Oops...',
              text: 'No name registered'
            });
          }else{
            this.$swal({
              type: 'error',
              title: 'Oops...',
              text: 'Error in occured'
            });
          }
          
        });
      },
      uploadFile($event) {
        this.spinner();
        var file = $event.target.files[0];
        var myReader = new FileReader();
        let _this = this;
        myReader.readAsDataURL(file);
        myReader.onloadend = e => {
          _this.embedding = myReader.result;
          myReader.readAsText(file);
        };

        setInterval(() => {
          if (this.embedding){
            this.cancelLoader()
          }
        }, 1000);
      }
    },
    mounted(){
      const input = document.getElementsByTagName('video')[0]
      var wid1 = (input.parentElement.offsetWidth);
      input.setAttribute('style', 'height: auto !important;width: '+wid1+'px !important;')
      var node = document.createElement("canvas"); 
      const canvas = document.getElementsByTagName('canvas')[0]
      canvas.parentElement.setAttribute('style', 'margin: 0; overflow:')
      canvas.parentElement.appendChild(node)
      // var wid = (input.parentElement.offsetWidth - 290) / 2;
      node.setAttribute('style', 'position: absolute; top: 0; left: 0; margin-left: ' + 22 + 'px; margin-top: ' + 20 + 'px')
      
      var objects = new tracking.ObjectTracker(['face']);
      objects.setInitialScale(4);
      objects.setStepSize(2);
      objects.setEdgesDensity(0.1);
      var trackerTask = tracking.track('video', objects);
      let lastCall = 0;
      let lastDraw = 0;
      let _this = this;

      objects.on('track', function(event) {
        if (event.data.length !== 0){
          event.data.forEach(function(rect) {
            const canvas = document.getElementsByTagName('canvas')[1]
            canvas.width = wid1
            canvas.height = input.parentElement.offsetHeight
            var ctx = canvas.getContext("2d");
            ctx.strokeStyle = "red";
            ctx.rect(rect.x, rect.y, rect.width, rect.height);
            ctx.stroke();
            lastDraw = new Date();
            if (new Date() - lastCall >= 500){
                  console.log("Pic Taken")
                  _this.picture= _this.$refs.camera.snapshot();
                  _this.pictureTaken =  true;
                  lastCall = new Date();
            }
          });
        } else {
          if (new Date() - lastCall >= 1300){
            lastDraw = new Date();
            const canvas = document.getElementsByTagName('canvas')[1]
            canvas.width = wid1
            canvas.height = input.parentElement.offsetHeight
            var ctx = canvas.getContext("2d");
            ctx.stroke();
          }
        }
      });
    }
  }
</script>

<style scoped>

.valid {
    border: 1px solid #42a948;
}

.notValid{
    border: 1px solid #a94442;
}


.loginImage{
    border: 5px solid #343a40;
    width: 100px;
    height: 100px;
    padding: 14px;
    margin: 5px;
    margin-top: 0px;
    border-radius: 100%;
}

.page{
  background-color: whitesmoke;
  height: 100vh;
}

.wrapper {
  display: flex;
  align-items: center;
  flex-direction: column; 
  justify-content: center;
  width: 100%;
  min-height: 100%;
  padding: 20px;
}

#formContent {
  -webkit-border-radius: 10px 10px 10px 10px;
  border-radius: 10px 10px 10px 10px;
  background: #fff;
  padding: 20px;
  width: 90%;
  max-width: 450px;
  position: relative;
  -webkit-box-shadow: 0 30px 60px 0 rgba(0,0,0,0.3);
  box-shadow: 0 30px 60px 0 rgba(0,0,0,0.3);
  text-align: center;
}

input {
  background-color: #f5f5f5;
  border: none;
  color: #0d0d0d;
  padding: 5px 10px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 5px;
  width: 95%;
  border: 2px solid #f5f5f5;
  -webkit-transition: all 0.5s ease-in-out;
  -moz-transition: all 0.5s ease-in-out;
  -ms-transition: all 0.5s ease-in-out;
  -o-transition: all 0.5s ease-in-out;
  transition: all 0.5s ease-in-out;
  -webkit-border-radius: 5px 5px 5px 5px;
  border-radius: 5px 5px 5px 5px;
}

button{
  width: 95%;
}

input:focus {
  background-color: #fff;
  border-bottom: 2px solid #5fbae9;
}

input:placeholder {
  color: #cccccc;
}


.fadeInDown {
  -webkit-animation-name: fadeInDown;
  animation-name: fadeInDown;
  -webkit-animation-duration: 1s;
  animation-duration: 1s;
  -webkit-animation-fill-mode: both;
  animation-fill-mode: both;
}

@-webkit-keyframes fadeInDown {
  0% {
    opacity: 0;
    -webkit-transform: translate3d(0, -100%, 0);
    transform: translate3d(0, -100%, 0);
  }
  100% {
    opacity: 1;
    -webkit-transform: none;
    transform: none;
  }
}

@keyframes fadeInDown {
  0% {
    opacity: 0;
    -webkit-transform: translate3d(0, -100%, 0);
    transform: translate3d(0, -100%, 0);
  }
  100% {
    opacity: 1;
    -webkit-transform: none;
    transform: none;
  }
}

@-webkit-keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
@-moz-keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
@keyframes fadeIn { from { opacity:0; } to { opacity:1; } }

.fadeIn {
  opacity:0;
  -webkit-animation:fadeIn ease-in 1;
  -moz-animation:fadeIn ease-in 1;
  animation:fadeIn ease-in 1;

  -webkit-animation-fill-mode:forwards;
  -moz-animation-fill-mode:forwards;
  animation-fill-mode:forwards;

  -webkit-animation-duration:1s;
  -moz-animation-duration:1s;
  animation-duration:1s;
}

.fadeIn.first {
  -webkit-animation-delay: 0.2s;
  -moz-animation-delay: 0.2s;
  animation-delay: 0.2s;
}

.fadeIn.second {
  -webkit-animation-delay: 0.4s;
  -moz-animation-delay: 0.4s;
  animation-delay: 0.4s;
}

.fadeIn.third {
  -webkit-animation-delay: 0.6s;
  -moz-animation-delay: 0.6s;
  animation-delay: 0.6s;
}

.fadeIn.fourth {
  -webkit-animation-delay: 0.8s;
  -moz-animation-delay: 0.8s;
  animation-delay: 0.8s;
}
.underlineHover:after {
  display: block;
  left: 0;
  bottom: -10px;
  width: 0;
  height: 2px;
  background-color: #56baed;
  content: "";
  transition: width 0.2s;
}

.underlineHover:hover {
  color: #0d0d0d;
}

.underlineHover:hover:after{
  width: 100%;
}

*:focus {
    outline: none;
} 

</style>
