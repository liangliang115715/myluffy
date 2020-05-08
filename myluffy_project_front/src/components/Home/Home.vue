<template>
<div>
  <el-carousel :interval="2000" arrow="always" height="540px">
    <el-carousel-item v-for="obj in lunboImgs" :key="obj.id">
      <img :src="obj.imgSrc" alt="">
    </el-carousel-item>
  </el-carousel>
</div>
</template>
<script>
  export default {
    name: "Home",
    data() {
      return {
        lunboImgs: [
          {
            id: 1,
            imgSrc:
              "https://hcdn1.luffycity.com/static/frontend/index/banner1(4)_1539945492.0492468.png"
          },
          {
            id: 2,
            imgSrc:
              "https://hcdn1.luffycity.com/static/frontend/index/骑士(1)_1539945488.713867.png"
          },
          {
            id: 3,
            imgSrc:
              "https://hcdn1.luffycity.com/static/frontend/index/banner11_1538122470.2779157.png"
          },
          {
            id: 4,
            imgSrc:
              "https://hcdn1.luffycity.com/static/frontend/index/home-banner4_1535545832.4715614.png"
          }
        ]
      };
    }
  };
</script>


<style lang="css" scoped>
  img {
    width: 100%;
    height: auto;
  }
</style>
