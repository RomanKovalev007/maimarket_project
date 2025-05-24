class Tab{

    selectors = {
       button: '[data-js-tabs-button]',
       content:  '[data-js-tabs-content]'
    }

    state = {
        isActive: 'is-active'
    }

    stateAttributes = {
        ariaSelected: 'aria-selected',
        tabIndex: 'tabindex'
    }


    updateUi(index){
    
        this.buttonsList.forEach((item, i)=>{
            const bollIndex = index === i
            item.classList.toggle(this.state.isActive, bollIndex)
        })

        
        this.contentList.forEach((item, i)=>{
            const bollIndex = index === i
            item.classList.toggle(this.state.isActive, bollIndex)
        })
    }

    onButtonClick(index){
        this.qurrentIndex.index = index
        this.updateUi(index)
    }

    bindEvents(){
        this.buttonsList.forEach((btn, index)=>{
            btn.addEventListener('click',()=>{
                this.onButtonClick(index)
            })
        })
    }
    constructor(item){
        this.rootTab = item
        this.buttonsList =  this.rootTab.querySelectorAll(this.selectors.button)
        this.contentList =  this.rootTab.querySelectorAll(this.selectors.content)

        this.qurrentIndex = {
            index:  [...this.buttonsList].findIndex((item)=>{
                return item.classList.contains(this.state.isActive)
            })
        }

        this.bindEvents()

    }
}








class TabLItst{
    tabs = '[data-js-tabs]'
    constructor(){
        const tabList = document.querySelectorAll(this.tabs)
        tabList.forEach((item)=>{
            new Tab(item)
        })
    }
}
new TabLItst()