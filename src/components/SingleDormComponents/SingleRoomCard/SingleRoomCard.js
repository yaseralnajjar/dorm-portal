export default {
  name: "SingleRoomCard",
  components: {
  },
  props: {
  },
  data: function () {
    return {
      savedRoom: null,
      showSavedRoomModel: false,
      showSavedRoomNav: true
    };
  },
  methods: {
    savedRoomFetch(){
      if(localStorage.getItem("room") != null){
        this.savedRoom = JSON.parse(localStorage.getItem("room"));
        this.showSavedRoomNav = true;
      }
    },
    deleteSavedRoom(){
      localStorage.removeItem("room");
      this.showSavedRoomNav = false;
    },
    showRoomModel(){
      this.showSavedRoomModel = true;
    },
    closeRoomModel(){
      this.showSavedRoomModel = false;
    },
    reserveRoom(room){
      if(this.$store.getters.isLoggedIn){
        this.$store.dispatch('reserveRoom', room).then(() => {
          this.$router.push('/reservation')
        })
      }else{
        localStorage.setItem("room", JSON.stringify({room}))
        this.$router.push('/reservation')
      }
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  },
  created(){
    this.savedRoomFetch();
  }
};