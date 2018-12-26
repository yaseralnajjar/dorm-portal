import DormMap from "../../SharedComponents/DormMap/DormMap.vue";

export default {
  name: "ManageDorm",
  components: {
    'dorm-map': DormMap
  },
  data: function () {
    return {
      active: null,
      items: ['Streaming', 'Eating'],
      selectedFeatures: [],
      isUpdating: false,
      loadingBtn: false,
      file: '',
      search: '',
      headers: [
        { text: 'id', value: 'id' },
        { text: 'Bank Name', value: 'bank_name'  },
        { text: 'Account Name', value: 'account_name' },
        { text: 'Account Number', value: 'account_number' },
        { text: 'Swift', value: 'swift' },
        { text: 'IBAN', value: 'iban' },
        { text: 'Currency', value: 'currency_code' },
        { text: 'Actions', value: 'id' }
      ],
      Features: [
        { name: 'Free wifi', id: 1},
        { name: 'Free parking', id: 2},
        { name: 'Hot water', id: 3},
        { name: 'Cold water', id: 4}
      ],
      bank:{
        name:'',
        accountName:'',
        accountNumber: '',
        swift:'',
        iban: '',
        currency: ''
      },
      dialog: {
        idHolder: null,
        isEdit: false,
        general: false,
        features: false,
        location: false,
        addBanks: false
      },
      deleteRecord:{
        confirmDialog: false,
        id: null
      },
      rowsPerPage: [10, 20, 30, 40],
      pagination: {
        rowsPerPage: 10,
        sortBy: 'id',
        descending : true
      },
      dormsAboutDesc:[1,2],
      requiredRules:[
        v => !!v || 'This field is required'
      ],
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid'
      ],
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    },
    languages(){
      return this.$store.state.languages;
    },
    currencies(){
      return this.$store.state.currencies;
    },
    dorm(){
      return this.$store.getters.manageDorm
    },
    dormId(){
      return localStorage.getItem('manageDormID')
    },
    bankAccounts(){
      return this.dorm.bank_accounts
    }
  },
  methods: {
    remove (item) {
      const index = this.selectedFeatures.indexOf(item.id)
      if (index >= 0) this.selectedFeatures.splice(index, 1)
    },
    resetFields(obj) {
      Object.keys(obj).forEach((key)=> {
          obj[key] = null
      })
    },
    fetchManagerDorm(){
      const dormID = localStorage.getItem('manageDormID')
      this.$store.dispatch("fetchManagerDorm", dormID).then((response)=>{
        let dormFeatures = []
        for(const feature of response.features){
          dormFeatures.push(feature.id)
        }
        this.selectedFeatures = dormFeatures
      })
      .catch(()=>{
        this.$store.state.snackbar.trigger = true
        this.$store.state.snackbar.message = 'Can\'t load dorm'
        this.$store.state.snackbar.color = 'error'
      })
    },
    formBind(dialogName,data){
      this.dialog['isEdit'] = true
      if(dialogName == 'addBanks'){
        this.dialog.idHolder = data.id
        this.bank.name = data.bank_name
        this.bank.accountName = data.account_name
        this.bank.accountNumber = data.account_number
        this.bank.swift = data.swift
        this.bank.currency = data.currency_code
        this.bank.iban = data.iban        
      }
    },
    updateDialog(dialogName, editAction, data){
      if(editAction == true){
        this.formBind(dialogName, data)
      }else{
        this.dialog['isEdit'] = false
      }
      this.dialog[dialogName] = true
    },
    closeDialog(dialogName){
      this.dialog[dialogName] = false
      if(dialogName == 'addBanks'){
        this.$refs.form.reset()
      }
    },
    UpdateDormInfo(data,dialog){
      if(this.$refs.form.validate()){
        this.loadingBtn = true
        this.$store.dispatch("updateDormInfo", data).then(()=>{
          let snackbar = {
            message: 'Updeated successfully',
            color: 'success'
          }
          this.$store.dispatch("fetchManagerDorm", this.dormId)
          this.closeDialog(dialog)
          this.$store.commit('updateSnackbar', snackbar)
        }).catch(()=>{
          let snackbar = {
            message: 'Something went wrong!, try again',
            color: 'error'
          }
          this.$store.commit('updateSnackbar', snackbar)
        }).then(()=>{
          this.loadingBtn = false
        })
      }
    },
    submitDormInfo(dialog){
      let about = []
      for(const lang in this.dorm.abouts){
        about.push({
          [lang] : this.dorm.abouts[lang]
        })
      }
      let data = {
        dormID: localStorage.getItem('manageDormID'),
        abouts: about,
        contact_name: this.dorm.contact_name,
        contact_number: this.dorm.contact_number,
        contact_fax: this.dorm.contact_fax,
        contact_email: this.dorm.contact_email,
      }
      this.UpdateDormInfo(data, dialog)
    },
    submitDormFeatures(dialog){
      let data = {
        dormID: localStorage.getItem('manageDormID'),
        features: this.selectedFeatures
      }
      this.UpdateDormInfo(data, dialog)
    },
    getGeolocation(){
      if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition((position)=>{
          position.enableHighAccuracy = true
          console.log(position)
          const lng = position.coords.longitude
          const lat = position.coords.latitude
          this.dorm.geo_longitude = lng
          this.dorm.geo_latitude = lat
        })
      } else {
        console.log('geolocation IS NOT available on your browser');
      }
    },
    submitDormLocation(dialog){
      let data = {
        dormID: localStorage.getItem('manageDormID'),
        geo_longitude: this.dorm.geo_latitude,
        geo_latitude: this.dorm.geo_longitude,
        address: this.dorm.address
      }
      this.UpdateDormInfo(data, dialog)
    },
    selectCover(){
      const file = this.$refs.coverFile.files[0]
      this.file = file
      
      const MAX_SIZE = 20000000
      const allowedType = ['image/jpeg', 'image/png', 'image/gif']
      const largeFile = file.size > MAX_SIZE
      const isAllowedType = allowedType.includes(file.type)
      const id = this.dormId
      const formData = new FormData()
      formData.append('cover', this.file)

      if(isAllowedType && !largeFile){
        this.$store.dispatch("uploadDormCover", {id,formData}).then(()=>{
          let snackbar = {
            message: 'Cover Updated Successfully',
            color: 'success'
          }
          this.$store.commit('updateSnackbar', snackbar)
          this.$store.dispatch("fetchManagerDorm", this.dormId)
        }).catch(()=>{
          let snackbar = {
            message: 'Some thing went wrong! try again',
            color: 'error'
          }
          this.$store.commit('updateSnackbar', snackbar)
        })
      }else{
        let message = isAllowedType ? `Max size is  ${MAX_SIZE/1000} KB` : 'Only images are allowed'
        let snackbar = {
          message: message,
          color: 'error'
        }
        this.$store.commit('updateSnackbar', snackbar)
      }      
    },
    submitNewBank(){
      const id = this.dormId
      let data = this.bank
      if(this.$refs.form.validate()){
        this.$store.dispatch("addBankAccount", {id, data}).then(() => {
          let snackbar = {
            message: 'Bank Account Added Successfully',
            color: 'success'
          }
          this.$store.dispatch("fetchManagerDorm", this.dormId)
          this.closeDialog('addBanks')
          this.$store.commit('updateSnackbar', snackbar)
        }).catch(() => {
          let snackbar = {
            message: 'Some thing went wrong! try again',
            color: 'error'
          }
          this.$store.commit('updateSnackbar', snackbar)
        })
      }
    },
    deleteBankAccount(){
      const accountId= this.deleteRecord.id
      const dormId = this.dormId
      this.$store.dispatch('deleteBankAccount', {dormId,accountId}).then(()=>{
        let snackbar = {
          message: 'Bank Account Has been Deleted Successfully',
          color: 'success'
        }
        this.$store.dispatch("fetchManagerDorm", this.dormId)
        this.deleteRecord.confirmDialog = false
        this.$store.commit('updateSnackbar', snackbar)
      }).catch(()=>{
        let snackbar = {
          message: 'Some thing went wrong! try again',
          color: 'error'
        }
        this.$store.commit('updateSnackbar', snackbar)
      })
    },
    confirmDelete(id){
      this.deleteRecord.confirmDialog = true
      this.deleteRecord.id = id
    },
    updateBankAccount(){
      const dormId = this.dormId
      const accountId = this.dialog.idHolder
      let data = this.bank
      if(this.$refs.form.validate()){
        this.$store.dispatch("updateBankAccount", {dormId, accountId, data}).then(() => {
          let snackbar = {
            message: 'Bank Account Updated Successfully',
            color: 'success'
          }
          this.$store.dispatch("fetchManagerDorm", this.dormId)
          this.closeDialog('addBanks')
          this.$store.commit('updateSnackbar', snackbar)
        }).catch(() => {
          let snackbar = {
            message: 'Some thing went wrong! try again',
            color: 'error'
          }
          this.$store.commit('updateSnackbar', snackbar)
        })
      }
    }
  },
  watch: {
    isUpdating (val) {
      if (val) {
        setTimeout(() => (this.isUpdating = false), 3000)
      }
    }
  },
  mounted(){
    this.fetchManagerDorm()
  }
};