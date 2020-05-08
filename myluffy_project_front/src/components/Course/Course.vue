<template>
  <div class="course">
    <div class="container clearfix">
      <ul class="coursebox">
        <li @click = 'categoryHandler(index,category.id)' v-for="(category,index) in categoryList" :key = 'category.id' :class = '{active:index===cureentIndex}'>
            {{ category.name }}
        </li>
        
      </ul>

      <div class="courseList">
          <!-- 课程列表 -->
        <div @click= 'courseHandler(course.id)' class="detail" v-for = '(course) in courseList' :key= 'course.id'>
          <div class="head">
            <img :src= 'course.course_img' alt class="backImg">
            <b class="mask" :style = '{background:course.colorName}'></b>
            <p>{{ course.name }}</p>
          </div>
          <div class="content">
            <p>{{ course.brief}}</p>
            <div class="content-detail">
              <div>
                <img
                  src="data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMTFweCIgaGVpZ2h0PSIxMnB4IiB2aWV3Qm94PSIwIDAgMTEgMTIiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8IS0tIEdlbmVyYXRvcjogU2tldGNoIDQ4LjIgKDQ3MzI3KSAtIGh0dHA6Ly93d3cuYm9oZW1pYW5jb2RpbmcuY29tL3NrZXRjaCAtLT4KICAgIDx0aXRsZT5TaGFwZTwvdGl0bGU+CiAgICA8ZGVzYz5DcmVhdGVkIHdpdGggU2tldGNoLjwvZGVzYz4KICAgIDxkZWZzPjwvZGVmcz4KICAgIDxnIGlkPSJSZWN0YW5nbGUtMiIgc3Ryb2tlPSJub25lIiBzdHJva2Utd2lkdGg9IjEiIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTE3LjAwMDAwMCwgLTkxLjAwMDAwMCkiPgogICAgICAgIDxnIGlkPSLkuKrkurrkuK3lv4MiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDE3LjAwMDAwMCwgOTEuMDAwMDAwKSIgZmlsbD0iIzlCOUI5QiIgZmlsbC1ydWxlPSJub256ZXJvIj4KICAgICAgICAgICAgPHBhdGggZD0iTTYuNzU4MjMwODEsNi42MjU2MzEwOCBMNC4yNDEzMzM5Miw2LjYyNTYzMTA4IEMxLjkwMjMxNTc1LDYuNjI1NjMxMDggMCw4LjQxNDM0Nzg0IDAsMTAuNjEzNjY4OSBMMCwxMC44NTAyOTE3IEMwLDEyIDEuODcxODkwNjUsMTIgNC4yNDEzMzM5MiwxMiBMNi43NTgyNDUzMiwxMiBDOS4wMzQ0NTQ2MSwxMiAxMSwxMiAxMSwxMC44NTAyOTE3IEwxMSwxMC42MTM2Njg5IEMxMSw4LjQxNDc3MDM2IDkuMDk3MTkwOTUsNi42MjU2MzEwOCA2Ljc1ODIzMDgxLDYuNjI1NjMxMDggWiBNNS4zNzQwNDEyNiw2LjMyMTI0MjAyIEM3LjIyNjIxNDM2LDYuMzIxMjQyMDIgOC43MzMxOTI0Nyw0LjkwMzU2Mjg4IDguNzMzMTkyNDcsMy4xNjA2Mjc4MiBDOC43MzMxOTI0NywxLjQxNzc3NDU0IDcuMjI2MjE0MzYsMCA1LjM3NDA0MTI2LDAgQzMuNTIxOTI2MiwwIDIuMDE0ODAzLDEuNDE4MDc0MzkgMi4wMTQ4MDMsMy4xNjA2OTU5NyBDMi4wMTQ4MDMsNC45MDMxODEyNSAzLjUyMTkyNjIsNi4zMjEyNDIwMiA1LjM3NDA0MTI2LDYuMzIxMjQyMDIgWiIgaWQ9IlNoYXBlIj48L3BhdGg+CiAgICAgICAgPC9nPgogICAgPC9nPgo8L3N2Zz4K"
                  alt
                >
                <span>{{ course.people_buy}}</span>
                <span>{{ course.level}}</span>
                <span class="span3" v-if="course.is_free">
                  <span class="s">{{ course.origin_price}}</span>
                  <span class="t">免费</span>
                </span>
                <span class="span4" v-else>{{ course.price}}</span>
              </div>
            </div>
          </div>
        </div>
       
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Course",
  data(){
      return {
          categoryList:[],//分类列表
          cureentIndex:0,
          courseList:[],//课程列表
          categoryId:0,
          colorsList:['darkorchid',"darkcyan","darkkhaki","darkorchid",'#00b4e4','darkorchid',"darkcyan","darkkhaki","darkorchid",'#00b4e4',
          'darkorchid',"darkcyan","darkkhaki","darkorchid",'#00b4e4','darkorchid',"darkcyan","darkkhaki","darkorchid",'#00b4e4','darkorchid',"darkcyan","darkkhaki","darkorchid",'#00b4e4']
      }
  },
  created(){
      this.getCategoryList();
      this.getCourseList()
  },
  methods:{
      //课程列表点击事件操作
      courseHandler(id){
          //1.跳转路由   编程式导航
          this.$router.push({
              name:'course_detail',
              params:{
                  courseId:id
              }
          })
      },
      //分类列表事件处理
      categoryHandler(index,categtory_id){
          this.cureentIndex = index;
          this.categoryId = categtory_id;
          //获取分类列表的数据
          this.getCourseList();
      },
      //获取分类列表
      getCategoryList(){
          this.$http.categoryList()
          .then(res=>{
              if(res.error_no === 0){
                  this.categoryList = res.data;
                  let firstCategory = {
                      id:0,
                      name:'全部',
                      category:0
                  };
                  this.categoryList.unshift(firstCategory)
              }
          })
          .catch(err=>{
              console.log(err);
          })
      },
      //获取课程列表
      getCourseList(){
          this.$http.courseList(this.categoryId)
          .then(res=>{
            //   console.log(res)
            if(res.error_no === 0){
                this.courseList = res.data;
                //$.each()
                this.courseList.forEach((element,index)=>{
                   element.colorName = this.colorsList[index]
                });
            }

          })
          .catch(err=>{
              console.log(err);
          })
      }
  }
};
</script>

<style lang="css" scoped>
.course {
  width: 100%;
  height: 1000px;
  background: #f3f3f3;
 

}
.coursebox {
  padding: 24px 0;
  font-size: 16px;
  color: #666;
  letter-spacing: 0.41px;
  font-family: PingFangSC-Regular;
  overflow: hidden;
}
ul li {
  float: left;
  margin-right: 24px;
  cursor: pointer;
}

ul li.active {
  color: #00b4e4;
}
.courseList {
  width: 100%;
  height: auto;
  overflow: hidden;
}
.detail {
  float: left;
  width: 248px;
  height: auto;
  margin-right: 16px;
  margin-bottom: 30px;
  position: relative;
  padding: 0 20px;
  background: #fff;
  box-shadow: 0 2px 6px 0 #e8e8e8;
  transition: all 0.2s linear;
  cursor: pointer;
}
.detail:hover {
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
  transform: translate3d(0, -3px, 0);
}
.detail:nth-of-type(4n) {
  margin-right: 0;
}
.head {
  width: 100%;

  height: 144px;
}
.detail .head img {
  width: 100%;
  height: 144px;
  position: absolute;
  left: 0;
  top: 0;
}
.detail .head b {
  width: 100%;
  height: 144px;
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0.9;
  background: #56cbc4;
}
.detail .head p {
  position: absolute;
  width: 248px;
  height: 144px;
  left: 0;
  top: 0;
  text-align: center;
  font-family: PingFangSC-Medium;
  font-size: 24px;
  color: #fff;
  overflow: hidden;
  display: flex;
  align-items: center;
  padding: 0 20px;
  justify-content: space-around;
}
.content {
  width: 248px;

  height: 118px;
  padding-top: 30px;
}
.content p {
  width: 100%;
  height: 39px;
  font-size: 12px;
  color: #666;
  cursor: pointer;
  letter-spacing: 0.6px;
  margin-bottom: 20px;
  font-family: PingFangSC-Regular;
  overflow: hidden;
}
.content-detail {
  width: 100%;
  height: 40px;
  line-height: 40px;
  position: relative;
}
.content-detail .span3 {
  position: absolute;
  right: 0;
}
.content-detail .span3 .s {
  text-decoration: line-through;
}
.content-detail .span4 {
  /*margin-left: 100px;*/
  position: absolute;
  right: 0;
  color: #fc0107;
}
.content-detail .span3 .t {
  color: #000;
  margin-left: 5px;
  text-decoration: none !important;
  color: #fc0107;
}
</style>
