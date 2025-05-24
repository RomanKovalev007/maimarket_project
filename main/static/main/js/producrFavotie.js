


// document.addEventListener('click',(event)=>{
//     const iconHeartElement = event.target.closest('div .icon--heart')
//     console.log(iconHeartElement)
//     if(iconHeartElement.classList.contains('icon--heart')){
//         iconHeartElement.classList.toggle('icon-red-heart')
//     }
// })

class FavoriteProduct{
    selectors = {
        rootElement: '[data-js-favorite-product]',
        mainSvgIcon: '[data-js-svg-icon]',
        mainPathIcon: '[data-js-path-icon]',
    }

    state = {
        isActive: 'is-active'
        
    }


    sendId(element){
        this.favoriteId =  element.id
        fetch(`api/change/${encodeURIComponent(this.favoriteId)}`)
        .then(response => response.json())
        .then(json => console.log(json))
        
    }

    onClick(event){

        this.svgIcon.forEach((icon)=>{
            if(event.target === icon){
                this.iconHeartElement.classList.toggle(this.state.isActive)
                this.favoriteId = this.iconHeartElement.closest(this.selectors.rootElement)
                this.sendId(this.favoriteId)
            }
        })

        this.pathIcon.forEach((icon)=>{
            if(event.target === icon){
                this.iconHeartElement.classList.toggle(this.state.isActive)
                this.favoriteId = this.iconHeartElement.closest(this.selectors.rootElement)
                this.sendId(this.favoriteId)

            } 
        })
       

       

    }   

    bindEvents(){
        document.addEventListener('click',(event)=>{
            this.iconHeartElement = event.target.closest(this.selectors.rootElement)
            this.onClick(event)
               
        })
    }

    constructor(){
        this.svgIcon = document.querySelectorAll(this.selectors.mainSvgIcon)
        this.pathIcon = document.querySelectorAll(this.selectors.mainPathIcon)
        this.bindEvents()
    }
}

export default FavoriteProduct