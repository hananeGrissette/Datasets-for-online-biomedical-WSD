
<h1># Datasets-for-online-biomedical-WSD </h1>

<h2> The aim of this study </h2>
<p> Sentiment analysis models are mostly used to evaluate the convoyed sentiments by patients’ narratives gathered from multiple information sources, assess positive or negative clinical outcomes or judge the impact of a drug and a medical condition.<br/> 
 Their effectiveness depends mainly on the Word Sense Disambiguation (WSD) method applied to the medical domain. Indeed, connotative meaning and sentiment associated with natural language concepts exhibit additional structural ambiguities including lack of multi-word concepts senses, multiple sense modalities of an individual concept, biomedical concepts abbreviations, pragmatic, and descriptive or nontechnical medical terms and multi-source health and medical data fusion issues. Biomedical meaning is only meaningful in reference to, and in distinction from, other meanings that need to be justified according to the context in which the concepts occur. <br/>
In this study, we develop a semisupervised features-fusion based approach for medical sense disambiguation, offering a significant rate of biomedical concept senses discrimination and seeking constraints from conjunctions of the positive or negative semantics of aspects-based sentiment information.

</p>
<h2> Datasets Samples </h2>
We collected varied patients generated narratives datasets from multi-source data plateforms : Microblogs such as Twitter and health-related forums such as Parkinson's Disease (PD). 
<h3> 1- Parkinson's disease forum data </h3>
<h4> Dataset Samples Overview</h4>
<p> 
<a href ='https://parkinsonsnewstoday.com/forums/' target="_blank"> Parkinson disease forum </a> 
is a forum for long-term degenerative disorder-related discussions. We chose this forum because of the controversy of Parkinson’s disease related-experiences and the difficulties to distill insights from these shared narratives. Indeed, PD affects an estimated seven to 10 million people and families 
worldwide. Reports pour daily into healthcare communities. We added some samples of data we collected.  </br>
<table border = "1">
  
   <th> 
     <td> Dataset's Name</td>
     <td> Discription</td>
     <td> Statistics </td>
   </th>
   
   <tr> 
  <td> Dataset_1</td>
     <td> Parkinson_data.csv </td>
     <td>  This dataset has four attributes : topics,links,voices,replies, and comments.
  <ul>
  <li>topics : A matter dealt within a forum, discourse, or conversation towards a PD-related subject.</li>
  <li>links: Links of the topic-related discussions page. </li>
  <li>voices : A voice messages</li>
   <li> comments: Posts and replies</li>
</ul>
  </td>
     <td> 1396 Topics with all related posts and replies in the period between 20 June,2020 and 20 August,2020.</td>
   </tr>
<tr>
  <td> Dataset_2</td>
     <td> Parkinson_data_2.csv </td>
     <td>  This dataset has four attributes : topics,links,voices,replies, and comments.
  <ul>
  <li>topics : A matter dealt within a forum, discourse, or conversation towards a PD-related subject.</li>
  <li>links: Links of the topic-related discussions page. </li>
  <li>voices : A voice messages</li>
   <li> comments: Posts and replies</li>
</ul>
  </td>
     <td> 1501 Topics with all related posts and replies in the period between first October,2020 and 5 November,2020.</td>
   </tr>
   </table>
   </p>
<h4> Python Code for gathering this data and Jupyter Notebook example</h4> Here we provide the code to collect and Preprocessing steps:
<ul>
 <li> <strong>Crawler Code :  </strong> Cor collecting tweetscan be found in file : <b> Step1_Data_forum_crawler.py </b> and notebook examples <b>Step1_Data_forum_crawler.ipynb</b> </li>
 <li><strong> Preprocessing Code :  </strong> Code can be found in file <b>Step2_data_forum.ipynb</b></li>
</ul>


<h3> 2-Twitter data </h3>
<h4> Dataset Samples Overview</h4>
Twitter is considered the preferable avenue of huge “superspreaders” of healthcare topics with 330 million monthly active.</br>
 </br>
<table border = "1">
  
   <th> 
     <td> Dataset's Name</td>
     <td> Discription</td>
     <td> Statistics </td>
   </th>
   
   <tr> 
     <td> Dataset1 </td>
     <td> </td>
     <td> </td>
   </tr>
  
  <tr> 
     <td> Dataset2</td>
     <td> </td>
     <td> </td>
   </tr>
   
   <tr> 
     <td> Dataset2</td>
     <td> </td>
     <td> </td>
   </tr>
   </table>

<h4>Python Code for gathering this data and Jupyter Notebook example</h4>
