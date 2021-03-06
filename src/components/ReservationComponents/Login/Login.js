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
        v => !!v || this.lang.rules.emailRequired,
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v.trim()) || this.lang.rules.emailValid
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
      
      if(this.$refs.form.validate()){
        let user = {
          email: this.email,
          password: this.password
        }
        this.$backend.$login(user).then(() => {
          return this.$store.dispatch('auth')
        })
        .then(response => {
          if(response.is_manager == true){
            this.$router.push('/manage')
          }
          else{
            this.$router.push('/reservation')
          }
        })
        .catch(err =>  this.errors = err.response.data)
      }
    },
    isForgotPassword(){
      this.forgotPassword = true
    },
    resetPassword(){
      this.$backend.$resetPassword(this.email).then(() => {
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