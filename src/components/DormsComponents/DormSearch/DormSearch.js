export default {
  name: "DormSearch",
  props:{
    'dutarion': Array,
    'category': Array
  },
  data: function () {
    return {
      chosenDutarion: null,
      chosenCategory: null
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    },
    defaultDormType(){
      if(this.category != null){
        return this.category[0].name
      }
    },
    defaultAcademicYear(){
      if(this.dutarion != null){
        return this.dutarion[0].name
      }
    }
  },
  methods: {
    search(){
      this.$store.state.userFilters.category = this.chosenCategory
      this.$store.state.userFilters.duration = this.chosenDutarion
      this.$store.dispatch('fetchSearchedDorms')
    }
  }
};