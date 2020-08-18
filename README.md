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
 if setstate is in no diff functins then they has no dependency with each other
 and can be consoled in each others scope.
