<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"  
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <head>
    <link rel="stylesheet" type="text/css" href="proviola.css" />
    <link href="coqdoc.css" type="text/css" rel="stylesheet" />      
    
    <script type = "text/javascript" src="http://code.jquery.com/jquery-latest.min.js" />
    <script type = "text/javascript">
      $(document).ready(function() {
        $(".command").mouseenter(function() {
          $(this).next(".output").fadeIn(5);
                   }).mouseleave(function() {
          $(this).next(".output").fadeOut(0);})
      });
    </script>
  </head>

  <body>
    <xsl:for-each select="movie/scenes">
        <xsl:apply-templates />
      </xsl:for-each>
  </body>
  </html>

</xsl:template>

<xsl:template match="frame">
  <xsl:param name="scene-type"/>
 
  <xsl:choose>
  <xsl:when test="$scene-type = 'doc'">
    <xsl:copy-of select = "command-coqdoc/node()"/>
  </xsl:when>
  <xsl:otherwise>
    <span class="command"><xsl:copy-of select = "command-coqdoc/node()"/></span>
    <div class="output"><pre><xsl:copy-of select="response/node()"/></pre></div>
  </xsl:otherwise>
  </xsl:choose>

</xsl:template>

<xsl:template match="frame-reference">
  <xsl:param name="scene-type">doc</xsl:param>
  <xsl:variable name = "ref">
    <xsl:value-of select="@framenumber" />
  </xsl:variable>
  <xsl:apply-templates select="/movie/film/frame[@framenumber = $ref]">
    <xsl:with-param name="scene-type" select="$scene-type"/>
  </xsl:apply-templates>
</xsl:template>

<xsl:template match="scene">
  <xsl:param name="scene-type">doc</xsl:param>
  <div>
    <xsl:for-each select="@*">
    </xsl:for-each>
    
    <xsl:apply-templates>
      <xsl:with-param name="scene-type">
        <xsl:value-of select="@class"/>
       </xsl:with-param>
     </xsl:apply-templates>
  </div> 
</xsl:template>
</xsl:stylesheet>
