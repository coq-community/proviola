<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <head>
    <link href="coqdoc.css" type="text/css" rel="stylesheet"/>
    <link href="moviola.css" type="text/css" rel="stylesheet"/>

    <script type = "text/javascript">
      var responses = new Array();

      function mouseover(id, scene) {
        set_response(get_response(id), scene);
      };

      function mouseout(scene) {
        set_response("", scene);
      };

      function set_array() {
        <xsl:for-each select="movie/film/frame">
          <xsl:variable name="data">
            <xsl:call-template name="replace">
              <xsl:with-param name="string">
                <xsl:value-of 
                  select="translate(response, '&#x0A;', '&#x09;') "/> 
              </xsl:with-param>
              <xsl:with-param name="from">&quot;</xsl:with-param>
              <xsl:with-param name="to">\"</xsl:with-param>
            </xsl:call-template>
          </xsl:variable>

          i = <xsl:value-of select="@frameNumber"/>;
          data = "<xsl:value-of select="$data"/>";
          responses[i]=data;
        </xsl:for-each>
      };
      
      function get_response(id) {
        return responses[id];
      };

      function set_response(response, scene) {
        goalId = "goal"+scene;
        elById = document.getElementById(goalId);
        if(elById){ 
          goalSpan = elById.getElementsByTagName("span")[0];
          goalSpan.innerHTML = response.replace(/&#x09;/g , '\n');
        }
      };
    </script>
  </head>

  <body onload="set_array()">
  <xsl:for-each select="movie/scenes">
    <xsl:apply-templates />
  </xsl:for-each>
  </body>
  </html>

</xsl:template>


<xsl:template match = "scene">
  <div>
    <xsl:attribute name="class">
      <xsl:value-of select="@class"/>
    </xsl:attribute>
    <xsl:choose>
    <xsl:when test="@class='code'">
      <xsl:apply-templates>
        <xsl:with-param name="sceneRef" select = "@sceneNumber" />
      </xsl:apply-templates>
    </xsl:when>
    <xsl:otherwise>
      <xsl:apply-templates/>
    </xsl:otherwise>
    </xsl:choose>
  </div>
  
  <xsl:if test="@class='code'">
  <div class="goal">
    <xsl:attribute name="id">
    <xsl:text>goal</xsl:text><xsl:value-of select="@sceneNumber"/>
    </xsl:attribute>
    <pre> 
      <span>
      </span>
     </pre>
  </div>
  </xsl:if>
</xsl:template>


<xsl:template match="div-reference">
  <xsl:param name="sceneRef">-1</xsl:param>
  <xsl:variable name="frame">
    <xsl:value-of select="@frame"/>
  </xsl:variable>
  <xsl:apply-templates select="/movie/film/frame[@frameNumber = $frame]">
    <xsl:with-param name="sceneRef" select="$sceneRef"/>
  </xsl:apply-templates>

</xsl:template>

<xsl:template match="frame">
  <xsl:param name="sceneRef"/>
 
  <xsl:choose>
  <xsl:when test="$sceneRef &lt; 0">
    <xsl:copy-of select = "command-coqdoc/div/node()"/>
  </xsl:when>
  <xsl:otherwise>
    <span class="command">
      <xsl:attribute name="onmouseout">
      mouseout(
         <xsl:value-of select="$sceneRef"/>
      )
      </xsl:attribute>
      <xsl:attribute name="onmouseover">
      mouseover(
         <xsl:value-of select="@frameNumber"/>,
         <xsl:value-of select="$sceneRef"/>
      )
      </xsl:attribute>
      <xsl:copy-of select = "command-coqdoc/div/node()"/>
    </span>
  </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="replace">
  <xsl:param name="string"/>
  <xsl:param name="from"/>
  <xsl:param name="to"/>
  <xsl:choose>
    <xsl:when test= "contains($string, $from)">
      <xsl:value-of select="substring-before($string, $from)"/>
      <xsl:text><xsl:value-of select="$to"/></xsl:text>
      <xsl:call-template name="replace">
        <xsl:with-param name="string" 
                        select="substring-after($string, $from)"/>
        <xsl:with-param name="from" select="$from"/>
        <xsl:with-param name="to" select="$to"/>
      </xsl:call-template>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="$string"/> 
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

</xsl:stylesheet>
