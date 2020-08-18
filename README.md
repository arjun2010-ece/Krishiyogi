# Krishiyogi
This application is primarily to help farmers.


********************************
 const addCategory = () => {
        setModal(!modal);
        // fetchKeywords(categoryText) // fetchkeywords will recv categoryText inside
        console.log("add :", categoryText); //categoryText is not set here but if consoled will give the value here
    }
 
 const handleCategoryChange = (e) => {
        setCategoryText(e.target.value); /categoryText is set here so if consoled will not give the value here.
        console.log("add :", categoryText); //no value as setstate is asynchronous here
    }
    
 <Input value={categoryText} onChange={handleCategoryChange} id="category" />
 <Button color="primary" onClick={addCategory}>OK</Button>
 
 Note::
 if setstate is in 2 diff functions then they has no dependency with each other
 and can be consoled in each others scope.



=======================================================================

on onclick listeners you can definately pass ids such as::

<span className="fa fa-close cursor" onClick={()=>deleteCategory(id)}></span>

and while deleting only use "FILTER" based on id by onClick


==============================================================
use of useeffect::
whenever you are conditionally running use-effect then you have to put state and all other state above it in dependency array

BUTBIUT BUT BUT it is used only in the scenario when two states or setstates are running inside the same function and whenever one setstae runs or value is set and you have to do something in that scenarios.



function add(){
    setModal(!modal);
    fetchKeywords(categoryText)
    setCategoryText("");
}

for example here if you want to run something after setModal then you can use  effects or after setCategory then you can run effects based on conditions but 
mind it when you run effects after setModal then in dependency array you have to put only modal as dependency.

but if you do run effects after setCategory then you run effects with the condition or dependency array having both modal and category.
