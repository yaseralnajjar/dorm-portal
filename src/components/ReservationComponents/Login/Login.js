export default {
  name: "Login",
  data: function() {
    return {
      show: false,
      forgotPassword: false,
      email: '',
      password: '',
      valid: false,
      emailSent: false,
      isEmailNotExist: false,
      errors: [],
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v.trim()) || 'E-mail must be valid'
      ]
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  },
  methods: {
    submit(){
      // if(this.$refs.form.validate()){
      //   this.$store.dispatch("login").then(response => {
      //     if(response.is_manager == true){
      //       this.$router.push('/manage')
      //     }
      //     else{
      //       this.$router.push('/reservation')
      //     }
      //   })
      //   .catch(function (error) {
      //     console.log(error)
      //   });
      // }

      if(this.$refs.form.validate()){
        let user = {
          email: this.email,
          password: this.password
        }
        this.$store.dispatch('login', user).then(response => {
          console.log("ok")
          this.$store.dispatch('auth').then(response => {
            console.log(response)
          })
          .catch(err => console.log(err.response.data))

        })
        .catch(err => this.errors = err.response.data)
      }

    },
    isForgotPassword(){
      this.forgotPassword = true
    },
    resetPassword(){
      this.$store.dispatch("resetPassword", this.email).then(() => {
        this.emailSent = true
      })
      .catch(() => {
        this.isEmailNotExist = true
      });
    },
    formValidate(){
      let isValid = true
      this.emailRules.forEach((rules) => { if (rules(this.email) !== true) { isValid = false } })
      this.valid = isValid
    }
  },
  updated(){
    this.formValidate();
  }
  
};